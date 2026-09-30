# Tests and proofs

## Three tests

| Test | Ask | Example consequence |
| --- | --- | --- |
| Specific judgment | What can readers decide after seeing this that they could not decide before? | Keep output showing the tool respecting a workload limit. Skip a generic terminal illustration. |
| Duplication | Is that answer already clear elsewhere? | Link the existing limitations paragraph instead of creating a second page. |
| Upkeep | What must change when behavior changes, and is the benefit worth it? | Keep a reproducible still for a one-command tool; skip a manually edited trailer of the same result. |

A keep needs a one-sentence reason. A skip is valid, including for visuals. Do not create a catalogue of rejected artifacts simply to show that the tests ran.

## Questions the project should answer

These are reader needs, not five new files:

- **Existence and behavior:** What actually runs, with which input, and what did it produce?
- **Clarity and choice:** Which details make the behavior understandable? This is design judgment, not proof of correctness.
- **Engineering:** Can a newcomer run the stated check and understand a relevant boundary?
- **Tradeoffs:** What does the project deliberately omit, and why?
- **Operation:** What remains experimental, needs credentials, or has not been exercised?

A capture records one observed state. It does not prove durability, security, performance or broad usefulness. A chart needs inputs, units, baseline and conditions. A small comparison is an example, not a success rate.

## README opening

Make four answers easy to find near the start without treating a line count as a layout measurement:

1. What the project does and whom it helps.
2. What works now and what is unfinished.
3. A real result: text output, usage example, screenshot, diagram or demo link.
4. The shortest useful next action.

Put prerequisites next to first use. Explain likely misunderstandings where relevant. Route visitors only when their goals differ. Preserve plain text for runnable commands and image meaning.

A rights or attribution gap needs concrete clarification before redistribution; do not select a license for material whose rights are unknown. Configuration examples belong to projects with configuration. A verify command should exercise relevant behavior rather than merely print success.

## Reader pass

Try first use from a disposable copy. Check changed links and rendered assets. Trace factual claims to actual results or explicit limitations. Confirm that kept artifacts answer distinct questions. Record blocked execution honestly and continue local work that remains possible.
