// Post-render: keep the book edition (docs/book/) through a full render of the deck.
//
// A full `quarto render` of this site empties its output folder, docs/, which also holds the
// book edition copied there by `make book-publish` (book/README.md). After a full render,
// restore docs/book/ as last committed, so rendering the deck never deletes or changes the
// book. To update the book, run `make book-publish` (or `make site`) after the deck.
if (Deno.env.get("QUARTO_PROJECT_RENDER_ALL")) {
  const tracked = await new Deno.Command("git", {
    args: ["ls-files", "--error-unmatch", "docs/book/index.html"],
    stdout: "null",
    stderr: "null",
  }).output();
  if (tracked.success) {
    const restore = await new Deno.Command("git", {
      args: ["checkout", "HEAD", "--", "docs/book"],
    }).output();
    if (!restore.success) {
      console.error(new TextDecoder().decode(restore.stderr));
      Deno.exit(1);
    }
    console.log("keep-book: restored docs/book/ from HEAD");
  } else {
    console.log("keep-book: docs/book/ is not committed yet; run `make book-publish`");
  }
}
