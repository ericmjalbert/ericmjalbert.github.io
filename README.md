# ericmjalbert.github.io

Personal website to act as a professional portfolio.

## Usage

### New draft post

Create a new draft post file from some basic templating:

```bash
TITLE="<POST_TITLE_HERE>"
SLUG="$(echo $TITLE | awk '{gsub(/ /, "_"); print tolower()}')"
NEW_POST="./content/__draft_$SLUG.md"
cp ./__template_draft.md $NEW_POST

sed "s/title-here/$TITLE/g" $NEW_POST \
    | sed "s/date-here/$(date '+%Y-%m-%d %H:%M:%S')/g" \
    | sed "s/modified-here/$(date '+%Y-%m-%d %H:%M:%S')/g" \
    | sed "s/slug-here/$SLUG/g" \
    > $NEW_POST
```

### Publishing a completed draft

Make sure the page looks good
```bash
make publish
make serve
```
Now inspect it at http://localhost:8000/

Commit the changes to github and https://app.netlify.com/sites/ericmjalbert/overview will build it with each commit (using `pelican content`).


## Notes

* Changes to `css` use `{{ SITE_URL }}` instead of local file system. So if I make any changes to the template I won't see it locally.
