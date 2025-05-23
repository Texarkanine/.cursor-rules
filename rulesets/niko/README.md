Based on the blog post at https://medium.com/@aashari/getting-better-results-from-cursor-ai-with-simple-rules-cbc87346ad88

1. `niko-core` is *always on*, and transforms your AI code assistant into a seasonsed senior dev.
2. `niko-request` should be added as the "Custom Instructions" in a "Niko" [Custom Mode](https://docs.cursor.com/chat/custom-modes) in Cursor.
3. `niko-refresh` should be added as the "Custom Instructions" in a "Niko Refresh" Custom Mode in Cursor.

The custom mode should have basically all tools and options enabled, so that it can really _oneshot_ ( ;) ) the task.

Use the regular "Niko" mode for planning and development. If it gets stuck, switch to "Niko Refresh" and ask it to reconsider. Then switch back to "Niko" for follow-ups.

You *can* directly reference the refresh mode in a prompt, e.g. 

    Please follow the instructions in @niko-refresh.mdc to troubleshoot the issue.

but it's probably easiser to put it in a mode.
