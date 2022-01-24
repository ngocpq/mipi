Each folder contains patches for a benchmark.
--
* [snippets_defects4j_APR](/benchmarks/snippets_defects4j_APR): contains the extracted code snippets of APR patches that fixing bugs in the Defects4J benchmark.
* [snippets_defects4j_DEV](/benchmarks/snippets_defects4j_DEV): contains the extracted code snippets of DEVELOPER patches for bugs in the Defects4J benchmark.
* [snippets_quixbugs_APR](/benchmarks/snippets_quixbugs_APR): contains the extracted code snippets of APR patches for bugs in the quixbugs benchmark.
* [snippets_quixbugs_APR](/benchmarks/snippets_quixbugs_APR): contains the extracted code snippets of DEVELOPER patches for bugs in the quixbugs benchmark.
* file [correctness_defects4J_patches.md](/benchmarks/correctness_defects4J_patches.md): the predicted and the ground truth correctness of APR patches for Defects4J benchmark.
* file [correctness_quixbugs_patches.md](/benchmarks/correctness_quixbugs_patches.md): the predicted and the ground truth correctness of APR patches for QuixBugs benchmark.
* file [PerfectFL_Patches.md](/benchmarks/PerfectFL_Patches.md): APR patches generated with perfect fault localization.

The structure of each benchmark is as follows:
--
* benchmark
  * <bug_id>
    * <bug_id>_<tool_id>_<patch_id>
      * origin: code snippets of original buggy program
      * patched: patched code snippets
    * <bug_id>_<tool_id>_<patch_id>
      * origin: code snippets of original buggy program
      * patched: patched code snippets
  * <bug_id>
      * <bug_id>_<tool_id>_<patch_id>
        * origin: code snippets of original buggy program
        * patched: patched code snippets
