# seoncafe.github.io

## Local preview

From the repository root:

```sh
python3 -m http.server 8765 --bind 127.0.0.1
```

Open <http://127.0.0.1:8765/>. Use the browser's responsive device mode or
resize its window to compare mobile and desktop layouts. No build is required.

## Responsive layout

`css/responsive.css` is the shared responsive layer, loaded after the Sitely
styles in all nine pages. Desktop layouts retain the generated positioning;
below 960px, content uses normal document flow with flexible widths and heights.
The navigation has five columns on larger screens and two below 600px.

The HTML adds semantic navigation and the `page-shell`, `site-header`,
`content-block`, and `site-footer` hooks. Images retain their original maximum
width through `--media-width`. The CV section also has a mobile ordering fix.

Sitely re-exporting can overwrite these HTML changes. Preserve these hooks,
the device-width viewport, and the shared stylesheet link when exporting again.

Before publishing, check all menu destinations, long publication and teaching
lists, image scaling, and both LaRT video controls at mobile and desktop widths.

## Teaching content

Run `python3 scripts/update_teaching.py` after editing lecture PDFs or course
metadata. The current Exoplanetary Atmospheres course and new courses use
`Teaching_files/<course>/course.json` and `lectures.csv`; older course archives
remain in the HTML. The script tracks PDF contents, updates dates in Korea time,
and renders the managed course section as static HTML.

See [Teaching 관리 안내](docs/TEACHING_GUIDE.md) for PDF replacement, schedule
changes, new lectures, new courses, local preview, and publishing instructions.

Run maintenance tests with `python3 -m unittest discover -s tests -v`.
