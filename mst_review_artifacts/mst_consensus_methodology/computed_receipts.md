## Arithmetic Receipts

### AR1
procedure_id: grim
evidence_anchor: text: §5 Distance from Intended Annotations, p. 7 "88.9% in India and 83.4% in the United States"
reported_inputs: 88.9% in India; 19 from the MST-E Golden Images or Challenging Image sets; One of the MST-E subjects was excluded from this study due to a programming error
assumptions: the paper defines the metric as the percentage of median MST annotations within 1-point of the oracle, i.e. a mean of per-image 0/1 indicators on [0,1], so 88.9% is transcribed as the proportion 0.889 (percent sign dropped, decimal point shifted two places, no rounding); n=36 is the paper-stated count of oracle-annotated expert images (19 subjects minus the 1 excluded per footnote 4, in both the Golden and Challenging sets; Appendix E Figure 7(a) and 7(b) each list 18 subjects); the paper reports one value per market with no per-set split and does not state the denominator explicitly; rounding rule not stated
derivation: an unweighted mean of N=36 integer responses on [0,1] must be an integer sum divided by 36; candidate sums range over [0,36]
derived_value_or_range: sum 32 gives 32/36 = 0.8889, which rounds to 0.889
comparison_rule: the reported mean 0.889 at 3 decimals is reachable only if some integer sum lands in its rounding interval under every conventional rounding rule (half-up, half-even)
status: consistent
rounding_interval: 0.8885 <= mean <= 0.8895 (interval interior; endpoint ties depend on the unstated rule, and a verdict is issued only where half-up and ties-to-even agree)
nearest_achievable: achieving sum 32; adjacent sums 32/36 = 0.8889; 33/36 = 0.9167

### AR2
procedure_id: grim
evidence_anchor: text: §5 Distance from Intended Annotations, p. 7 "88.9% in India and 83.4% in the United States"
reported_inputs: 83.4% in the United States; 19 from the MST-E Golden Images or Challenging Image sets; One of the MST-E subjects was excluded from this study due to a programming error
assumptions: the paper defines the metric as the percentage of median MST annotations within 1-point of the oracle, i.e. a mean of per-image 0/1 indicators on [0,1], so 83.4% is transcribed as the proportion 0.834 (percent sign dropped, decimal point shifted two places, no rounding); n=36 is the paper-stated count of oracle-annotated expert images (19 subjects minus the 1 excluded per footnote 4, in both the Golden and Challenging sets; Appendix E Figure 7(a) and 7(b) each list 18 subjects); the paper reports one value per market with no per-set split and does not state the denominator explicitly; rounding rule not stated
derivation: an unweighted mean of N=36 integer responses on [0,1] must be an integer sum divided by 36; candidate sums range over [0,36]
derived_value_or_range: no integer sum in [0,36] rounds to 0.834 at 3 decimals
comparison_rule: the reported mean 0.834 at 3 decimals is reachable only if some integer sum lands in its rounding interval under every conventional rounding rule (half-up, half-even)
status: mismatch
rounding_interval: 0.8335 <= mean <= 0.8345 (interval interior; endpoint ties depend on the unstated rule, and a verdict is issued only where half-up and ties-to-even agree)
nearest_achievable: 30/36 = 0.8333; 31/36 = 0.8611

### AR3
procedure_id: grim
evidence_anchor: text: §5 Distance from Intended Annotations, p. 7 "0.78 in India and 0.84 in the United States"
reported_inputs: 0.78 in India; computed across all images; five experts in photography in India; Each expert reviewed each image; 19 from the MST-E Golden Images or Challenging Image sets; One of the MST-E subjects was excluded from this study due to a programming error
assumptions: items are per-image differences between the median of the 5 India experts' MST ratings (each expert rated each image, so the median is an MST integer) and the integer oracle MST value; n=36 oracle-annotated images (18 subjects after the footnote-4 exclusion, Golden and Challenging sets) with the denominator not stated explicitly; the paper does not state whether the difference is absolute or signed, so the item range is not stated; rounding rule not stated
derivation: stopped before derivation: the response-scale support is not reported
derived_value_or_range: none (procedure stopped)
comparison_rule: none (no comparison was licensed)
status: not_computable
not_computable_reason: scale_support_unknown

### AR4
procedure_id: grim
evidence_anchor: text: §5 Distance from Intended Annotations, p. 7 "0.78 in India and 0.84 in the United States"
reported_inputs: 0.84 in the United States; computed across all images; five experts in photography in the United States; Each expert reviewed each image; 19 from the MST-E Golden Images or Challenging Image sets; One of the MST-E subjects was excluded from this study due to a programming error
assumptions: items are per-image differences between the median of the 5 US experts' MST ratings (each expert rated each image, so the median is an MST integer) and the integer oracle MST value; n=36 oracle-annotated images (18 subjects after the footnote-4 exclusion, Golden and Challenging sets) with the denominator not stated explicitly; the paper does not state whether the difference is absolute or signed, so the item range is not stated; rounding rule not stated
derivation: stopped before derivation: the response-scale support is not reported
derived_value_or_range: none (procedure stopped)
comparison_rule: none (no comparison was licensed)
status: not_computable
not_computable_reason: scale_support_unknown

### AR5
procedure_id: grim
evidence_anchor: text: §6 Distance from Intended Annotations, p. 8 "the consensus annotation agreed within 1 point for all but one subject (94.7%)"
reported_inputs: all but one subject (94.7%); Using the global pool; consisting of images from 19 subjects; annotations for the entire MST-E dataset
assumptions: per-subject 0/1 indicators of the global-pool Per Subject consensus being within 1 point of the oracle, on [0,1], so 94.7% is transcribed as the proportion 0.947 (percent sign dropped, decimal point shifted two places, no rounding); n=19 is the paper-stated MST-E subject count, all annotated by the crowdsourced pool with no exclusion stated for this study; rounding rule not stated
derivation: an unweighted mean of N=19 integer responses on [0,1] must be an integer sum divided by 19; candidate sums range over [0,19]
derived_value_or_range: sum 18 gives 18/19 = 0.9474, which rounds to 0.947
comparison_rule: the reported mean 0.947 at 3 decimals is reachable only if some integer sum lands in its rounding interval under every conventional rounding rule (half-up, half-even)
status: consistent
rounding_interval: 0.9465 <= mean <= 0.9475 (interval interior; endpoint ties depend on the unstated rule, and a verdict is issued only where half-up and ties-to-even agree)
nearest_achievable: achieving sum 18; adjacent sums 17/19 = 0.8947; 18/19 = 0.9474

### AR6
procedure_id: grim
evidence_anchor: text: §6 Distance from Intended Annotations, p. 8 "The distance was 0.78 for both well lit and poorly lit images."
reported_inputs: The distance was 0.78 for both well lit and poorly lit images; computed across all images; Each task was replicated 5 times in each region resulting in 25 annotations per image; Some images were too hard to annotate and were skipped by some annotators
assumptions: the paper does not state which annotator pool (global or a region) this value refers to, nor whether well lit images means the 19-image Golden set or all well-lit MST-E images, so n is not stated; skipped annotations can leave fewer than 25 (or 5) ratings per image, so integer median granularity is not licensed, and the sign convention of the distance is not stated, so the item range is not stated; rounding rule not stated
derivation: stopped before derivation: the item-specific analytic N is not reported
derived_value_or_range: none (procedure stopped)
comparison_rule: none (no comparison was licensed)
status: not_computable
not_computable_reason: analytic_n_ambiguous

### AR7
procedure_id: grim
evidence_anchor: text: §6 Distance from Intended Annotations, p. 8 "The distance was 0.78 for both well lit and poorly lit images."
reported_inputs: The distance was 0.78 for both well lit and poorly lit images; computed across all images; Each task was replicated 5 times in each region resulting in 25 annotations per image; Some images were too hard to annotate and were skipped by some annotators
assumptions: the paper does not state which annotator pool (global or a region) this value refers to, nor whether poorly lit images means the 19-image Challenging set or all poorly lit MST-E images, so n is not stated; skipped annotations can leave fewer than 25 (or 5) ratings per image, so integer median granularity is not licensed, and the sign convention of the distance is not stated, so the item range is not stated; rounding rule not stated
derivation: stopped before derivation: the item-specific analytic N is not reported
derived_value_or_range: none (procedure stopped)
comparison_rule: none (no comparison was licensed)
status: not_computable
not_computable_reason: analytic_n_ambiguous

### AR8
procedure_id: p_from_test_statistic
evidence_anchor: text: §6 Regional Differences in Annotation, p. 8 "(Pillai’s trace = 1.97,p< 0.05)"
reported_inputs: Pillai’s trace = 1.97,p< 0.05; multivariate analysis of variance (MANOVA) with annotator region as the independent variable and MST annotations for each subject as the dependent variable
assumptions: the only statistic printed is Pillai's trace, which is not a t, z, F, or chi-square value; the paper reports neither the approximating F statistic nor its df, so test family, statistic, and df are not stated; no tail convention stated
derivation: stopped before derivation: the test family is not identifiable from the report
derived_value_or_range: none (procedure stopped)
comparison_rule: none (no comparison was licensed)
status: not_computable
not_computable_reason: test_family_ambiguous
tail_convention: unstated

### AR9
procedure_id: p_from_test_statistic
evidence_anchor: text: §6 Extension to In-the-Wild Annotations, p. 8 "χ2 = 0.26, p = 0.99 > 0.05"
reported_inputs: χ2 = 0.26, p = 0.99 > 0.05; the intraclass correlation from the Open Images dataset has no significant differences than crowdsource annotators intraclass correlation in the MST-E dataset
assumptions: chi-square family as printed; the specific chi-square test used to compare the intraclass correlations is not named and its df is not reported; the paper states no tail convention
derivation: stopped before derivation: the degrees of freedom are not reported
derived_value_or_range: none (procedure stopped)
comparison_rule: none (no comparison was licensed)
status: not_computable
not_computable_reason: missing_reported_value
tail_convention: unstated

### AR10
procedure_id: p_from_test_statistic
evidence_anchor: text: §6 Extension to In-the-Wild Annotations, p. 8 "(V 2 = 0.0766,p < 0.05)"
reported_inputs: V 2 = 0.0766,p < 0.05; We also find significant differences between annotation distributions between regions
assumptions: the paper does not name the statistic printed as V 2 or the test that produced the p-value, so the test family is not stated; df not reported; no tail convention stated
derivation: stopped before derivation: the test family is not identifiable from the report
derived_value_or_range: none (procedure stopped)
comparison_rule: none (no comparison was licensed)
status: not_computable
not_computable_reason: test_family_ambiguous
tail_convention: unstated
