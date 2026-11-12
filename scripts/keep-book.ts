// Post-render: put back the book edition (docs/book/) after a full render of the deck.
//
// A full `quarto render` of this site empties its output folder, docs/, before anything else
// runs, which deletes the book edition copied there by `make book-publish` (book/README.md).
// After a full render, this restores docs/book/ from git's index: the committed version, or
// the staged one if docs/book/ was staged. Unstaged changes to docs/book/ cannot be recovered
// here; `make deck` copies docs/book/ aside before rendering and keeps them too.
if (Deno.env.get("QUARTO_PROJECT_RENDER_ALL")) {
  const git = (args: string[]) =>
    new Deno.Command("git", { args, stdout: "piped", stderr: "piped" }).output();
  const tracked = await git(["ls-files", "--error-unmatch", "docs/book/index.html"]);
  if (!tracked.success) {
    console.log("keep-book: docs/book/ is not in git yet; run `make book-publish`");
  } else {
    const restore = await git(["checkout", "--", "docs/book"]);
    if (!restore.success) {
      console.error(new TextDecoder().decode(restore.stderr));
      Deno.exit(1);
    }
    console.log("keep-book: restored docs/book/ from git (committed or staged)");
    // Say so if the last book build differs from what is now in docs/book/.
    const built = await git(["diff", "--no-index", "--quiet", "book/_book/html/index.html",
      "docs/book/index.html"]);
    if (built.code === 1) {
      console.log("keep-book: book/_book/html differs from docs/book/; run `make book-publish` " +
        "to publish it");
    }
  }
}
