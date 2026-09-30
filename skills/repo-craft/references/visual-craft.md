# Visual craft

Choose an image because it explains this project. Appearance is not proof that the product works. Capture an actual result, retain its source, and state what was observed.

| Project | Useful surface | When text is enough |
| --- | --- | --- |
| Visible application | A real screen from the task a newcomer cares about | The claimed task does not work yet; describe its current state. |
| Command line tool | Actual command and output with reproducible input | A short usage example communicates the whole result. |
| Data or model project | Actual outputs under identical inputs and conditions | No valid comparison exists yet; state that limit. |
| Library, collection or essay | Usage example, generated output or necessary explanatory diagram | A decorative banner would communicate only a category. |

Never fabricate a product screen. Label mockups and illustrative diagrams. A caption states a narrow claim: “The planner respects Mira's two-task limit in this fictional household” is checkable; “Intelligent planning at scale” is not.

## Capture process

1. Use a specific scenario and explicitly synthetic data. Use reserved domains such as `example.com`; invented plausible domains may belong to real people.
2. Retain input, command or interaction, environment and actual output. Keep full text beside a terminal image.
3. Frame the result with enough context. Never crop away an error while claiming a complete successful run. Label excerpts.
4. Inspect the asset at its displayed size. Keep text readable, provide useful alt text and a caption, and keep runnable commands outside images.
5. Retain the source and regeneration command. For multiple images, consistent scenario and cropping help readers compare them.

The [terminal renderer](../scripts/terminal_to_svg.py) formats text; it neither runs nor authenticates that transcript. Inspect the finished output. See [producer handoff](producer-handoff.md).

## Optional artifacts

**Hero.** Keep one when a prominent visual explains the core task better than text.

**Social preview.** Keep one when link sharing matters and project-specific evidence improves recognition. The bundled poster is 1280x640, a local format choice rather than a universal host requirement. Verify the destination's requirements before uploading. Storing a preview in Git does not configure the host.

**Diagram.** Explain a non-obvious transformation or boundary in the actual implementation. A directory tree alone rarely needs redrawing.

**Motion.** Use it when sequence, feedback or transitions carry meaning a still cannot show. Include accessible text or a still fallback. Narration that carries information needs captions. An instantaneous command may need no video.

**Identity.** Type, color and crop consistency are taste choices, not maturity requirements. Do not require a wordmark, custom domain, profile pin or palette family across unrelated projects.

Do not infer privacy properties from where a video is hosted. Check actual destination behavior when an authorized upload requires it. Follow [publication](publication.md).
