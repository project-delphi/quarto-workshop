# Listing the book in Apple Books and Google Play Books

So that iPhone and Android readers get the book with one tap ("Get"), with no file to find.
Both listings are free. The website edition and the GitHub downloads stay as they are.

Requirements checked on Apple's and Google's own pages on 2026-11-16 (links below). Stores
change their rules: read the linked page again if a step here no longer matches.

## Live listings

Both editions are on Apple Books, free, since 2026-11-17, in every storefront checked
(us, co, gb, es, mx; iTunes lookup API, 2026-11-21):

- English: <https://books.apple.com/us/book/prompt-check-publish/id6835827715>
- Spanish: <https://books.apple.com/co/book/pide-revisa-publica/id6835859903>

The landing pages' buttons read these from `APPLE_BOOKS` in `ebook/_source.py`; change them
there, then rerun `make ebook-media STEPS=head` (and `EDITION=es`) for the JSON-LD.

## 1. Make the files (the agent can run this)

```bash
make book-store
```

It makes, from the published EPUBs in `docs/book/`, one folder per edition in
`book/_book/store/` (`en/`, `es/`), each holding:

- the store EPUB (`*-store.epub`): the published book with each animated GIF replaced by its
  first frame, which is the book's own still (Apple takes only JPEG and PNG images, Google
  only static GIFs); it must pass EPUBCheck with no warnings, as `make book-store` checks;
- `cover.png`, 1600 × 2560 (Apple asks for at least 1400 px on the short side, Google at
  least 640 px);
- `listing.md`: every field the stores ask for, read from the EPUB (title, subtitle, author,
  description, AI disclosure, language, date, subjects), ready to copy.

Rerun it after each `make book-publish`, and upload the new file as an update to the listing.

## 2. Apple Books (iPhone, iPad, Mac)

Done by the author, in a browser:

1. Sign in at [Apple Books for Authors](https://authors.apple.com/) with your Apple Account and
   create the iTunes Connect account it asks for
   ([how](https://authors.apple.com/support/3967-create-itunes-connect-account)).
2. In iTunes Connect, Agreements: accept the **Free Books Agreement** only. A free book needs
   no tax or banking details.
3. Add a new book (Apple's Pages guide:
   [submit your book](https://itunespartner.apple.com/books/support/18-submit-your-book)).
   Upload `en/prompt-check-publish-store.epub` and `en/cover.png`, and copy the fields from
   `en/listing.md`. Set the price to free. Leave the ISBN empty: Apple says ISBNs are optional,
   and the Vendor ID in `listing.md` identifies the book
   ([metadata](https://itunespartner.apple.com/books/support/12-metadata)).
4. Paste both paragraphs of the description: Apple's
   [formatting guidelines](https://help.apple.com/itc/applebooksstoreformatting/en.lproj/static.html)
   (1.13, 4.8) ask for books with a material AI-generated portion to say so in the
   description, and the book's own AI usage statement is that disclosure.
5. Repeat for the Spanish edition (`es/`), as a separate book: Apple asks that a book's
   language match its text.

**Risk to know about.** Apple's
[asset guide](https://help.apple.com/itc/booksassetguide/en.lproj/itca71ad3c33.html) says
"books with images that contain embedded text are rejected from sale". This book's terminal
screenshots and charts carry text. Apple's reason is pictures of prose (a reader cannot search
or look up their words); this book's figures are screenshots and charts, each with alt text,
but a reviewer may still reject it. If Apple does, its message says which images; reply that
they are screenshots of software, which the text describes in full.

## 3. Google Play Books (Android)

Done by the author, in a browser:

1. Sign up for the [Partner Center](https://play.google.com/books/publish/) with a Google
   Account ([who can](https://support.google.com/books/partner/answer/4492574)).
2. Fill in the payment profile it asks for. For free books Google still wants a payment
   profile with an address, but no bank account
   ([pricing](https://support.google.com/books/partner/answer/6009574)).
3. Add a book; choose a Google book ID (GGKEY) instead of an ISBN
   ([add a book](https://support.google.com/books/partner/answer/9261664)). Upload
   `en/prompt-check-publish-store.epub` and `en/cover.png`; copy title, subtitle, description,
   language and the BISAC subjects from `en/listing.md`.
4. Pricing: a list price of 0 for all countries. Google requires free books to allow a
   preview on Google Books: leave it on.
5. Repeat for the Spanish edition, as a separate book.

**Risk to know about.** Google's
[content policy](https://support.google.com/books/partner/answer/1067634) says: "We do not
allow content that is easily found online at no charge". The website edition is exactly that.
The same page allows exceptions on "educational" grounds, which this book can fairly claim (it
is a course book for a free workshop), but a rejection is likely. A rejection costs nothing: if
it comes, keep the phone hints on the landing page as the Android route.

## After a listing goes live

Send the agent the store links. It adds "Apple Books" and "Google Play" buttons to the
landing page (`ebook/`) beside the download, on the phones each store serves.
