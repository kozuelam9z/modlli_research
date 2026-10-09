import Foundation
import Vision
import ImageIO
import UniformTypeIdentifiers
// usage: landmarks <listfile: lines "subject\tpath"> <outdir> <maxdim>
let a = CommandLine.arguments
let lines = try! String(contentsOfFile: a[1], encoding: .utf8).split(separator: "\n")
let outdir = a[2]; let maxdim = Int(a[3])!
var results: [[String: Any]] = []
func pts(_ r: VNFaceLandmarkRegion2D?, _ w: Int, _ h: Int) -> [[Double]] {
  guard let r = r else { return [] }
  return r.pointsInImage(imageSize: CGSize(width: w, height: h)).map { [Double($0.x), Double(h) - Double($0.y)] }
}
for (i, line) in lines.enumerated() {
  let parts = line.split(separator: "\t").map(String.init)
  let subj = parts[0], path = parts[1]
  let name = (path as NSString).lastPathComponent
  var rec: [String: Any] = ["subject": subj, "file": name]
  guard let src = CGImageSourceCreateWithURL(URL(fileURLWithPath: path) as CFURL, nil) else { rec["error"] = "open"; results.append(rec); continue }
  let opts: [CFString: Any] = [kCGImageSourceCreateThumbnailFromImageAlways: true, kCGImageSourceCreateThumbnailWithTransform: true, kCGImageSourceThumbnailMaxPixelSize: maxdim]
  guard let img = CGImageSourceCreateThumbnailAtIndex(src, 0, opts as CFDictionary) else { rec["error"] = "thumb"; results.append(rec); continue }
  let w = img.width, h = img.height
  let outName = "\(subj)__\(name).png"
  let dest = CGImageDestinationCreateWithURL(URL(fileURLWithPath: "\(outdir)/img/\(outName)") as CFURL, UTType.png.identifier as CFString, 1, nil)!
  CGImageDestinationAddImage(dest, img, nil); CGImageDestinationFinalize(dest)
  rec["out"] = outName; rec["w"] = w; rec["h"] = h
  let req = VNDetectFaceLandmarksRequest()
  let handler = VNImageRequestHandler(cgImage: img, options: [:])
  do { try handler.perform([req]) } catch { rec["error"] = "vision"; results.append(rec); continue }
  var faces: [[String: Any]] = []
  for f in (req.results ?? []) {
    let bb = f.boundingBox
    var fd: [String: Any] = ["bbox": [Double(bb.minX)*Double(w), Double(h)-Double(bb.maxY)*Double(h), Double(bb.width)*Double(w), Double(bb.height)*Double(h)], "conf": Double(f.confidence)]
    if let lm = f.landmarks {
      fd["faceContour"] = pts(lm.faceContour, w, h); fd["leftEye"] = pts(lm.leftEye, w, h); fd["rightEye"] = pts(lm.rightEye, w, h)
      fd["leftEyebrow"] = pts(lm.leftEyebrow, w, h); fd["rightEyebrow"] = pts(lm.rightEyebrow, w, h)
      fd["nose"] = pts(lm.nose, w, h); fd["outerLips"] = pts(lm.outerLips, w, h); fd["medianLine"] = pts(lm.medianLine, w, h)
    }
    if let yaw = f.yaw { fd["yaw"] = yaw.doubleValue }
    faces.append(fd)
  }
  rec["faces"] = faces
  results.append(rec)
  if i % 100 == 0 { FileHandle.standardError.write("\(i)\n".data(using: .utf8)!) }
}
let data = try! JSONSerialization.data(withJSONObject: results, options: [])
try! data.write(to: URL(fileURLWithPath: "\(outdir)/landmarks.json"))
print("done", results.count)
