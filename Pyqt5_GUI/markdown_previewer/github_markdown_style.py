GITHUB_MARKDOWN_STYLE = """
  /*
  Copyright (c) 2017 Chris Patuzzo
  https://twitter.com/chrispatuzzo
  Permission is hereby granted, free of charge, to any person obtaining a copy
  of this software and associated documentation files (the "Software"), to deal
  in the Software without restriction, including without limitation the rights
  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
  copies of the Software, and to permit persons to whom the Software is
  furnished to do so, subject to the following conditions:
  The above copyright notice and this permission notice shall be included in all
  copies or substantial portions of the Software.
  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
  SOFTWARE.
  */

  body {
    font-family: Helvetica, arial, sans-serif;
    font-size: 14px;
    line-height: 1.6;
    padding-top: 10px;
    padding-bottom: 10px;
    background-color: white;
    padding: 30px;
    color: #333;
  }

  body > *:first-child {
    margin-top: 0 !important;
  }

  body > *:last-child {
    margin-bottom: 0 !important;
  }

  a {
    color: #4183C4;
    text-decoration: none;
  }

  a.absent {
    color: #cc0000;
  }

  a.anchor {
    display: block;
    padding-left: 30px;
    margin-left: -30px;
    cursor: pointer;
    position: absolute;
    top: 0;
    left: 0;
    bottom: 0;
  }

  a:hover {
    text-decoration: underline;
  }

  h1, h2, h3, h4, h5, h6 {
    margin: 20px 0 10px;
    padding: 0;
    font-weight: bold;
    -webkit-font-smoothing: antialiased;
    cursor: text;
    position: relative;
  }

  h2:first-child, h1:first-child, h1:first-child + h2, h3:first-child, h4:first-child, h5:first-child, h6:first-child {
    margin-top: 0;
    padding-top: 0;
  }

  h1:hover a.anchor, h2:hover a.anchor, h3:hover a.anchor, h4:hover a.anchor, h5:hover a.anchor, h6:hover a.anchor {
    text-decoration: none;
  }

  h1 tt, h1 code {
    font-size: inherit;
  }

  h2 tt, h2 code {
    font-size: inherit;
  }

  h3 tt, h3 code {
    font-size: inherit;
  }

  h4 tt, h4 code {
    font-size: inherit;
  }

  h5 tt, h5 code {
    font-size: inherit;
  }

  h6 tt, h6 code {
    font-size: inherit;
  }

  h1 {
    font-size: 28px;
    color: black;
  }

  h2 {
    font-size: 24px;
    border-bottom: 1px solid #cccccc;
    color: black;
  }

  h3 {
    font-size: 18px;
  }

  h4 {
    font-size: 16px;
  }

  h5 {
    font-size: 14px;
  }

  h6 {
    color: #777777;
    font-size: 14px;
  }

  p, blockquote, ul, ol, dl, li, table, pre {
    margin: 15px 0;
  }

  hr {
    border: 0 none;
    color: #cccccc;
    height: 4px;
    padding: 0;
  }

  body > h2:first-child {
    margin-top: 0;
    padding-top: 0;
  }

  body > h1:first-child {
    margin-top: 0;
    padding-top: 0;
  }

  body > h1:first-child + h2 {
    margin-top: 0;
    padding-top: 0;
  }

  body > h3:first-child, body > h4:first-child, body > h5:first-child, body > h6:first-child {
    margin-top: 0;
    padding-top: 0;
  }

  a:first-child h1, a:first-child h2, a:first-child h3, a:first-child h4, a:first-child h5, a:first-child h6 {
    margin-top: 0;
    padding-top: 0;
  }

  h1 p, h2 p, h3 p, h4 p, h5 p, h6 p {
    margin-top: 0;
  }

  li p.first {
    display: inline-block;
  }

  ul, ol {
    padding-left: 30px;
  }

  ul :first-child, ol :first-child {
    margin-top: 0;
  }

  ul :last-child, ol :last-child {
    margin-bottom: 0;
  }

  dl {
    padding: 0;
  }

  dl dt {
    font-size: 14px;
    font-weight: bold;
    font-style: italic;
    padding: 0;
    margin: 15px 0 5px;
  }

  dl dt:first-child {
    padding: 0;
  }

  dl dt > :first-child {
    margin-top: 0;
  }

  dl dt > :last-child {
    margin-bottom: 0;
  }

  dl dd {
    margin: 0 0 15px;
    padding: 0 15px;
  }

  dl dd > :first-child {
    margin-top: 0;
  }

  dl dd > :last-child {
    margin-bottom: 0;
  }

  blockquote {
    border-left: 4px solid #dddddd;
    padding: 0 15px;
    color: #777777;
  }

  blockquote > :first-child {
    margin-top: 0;
  }

  blockquote > :last-child {
    margin-bottom: 0;
  }

  table {
    padding: 0;
  }
  table tr {
    border-top: 1px solid #cccccc;
    background-color: white;
    margin: 0;
    padding: 0;
  }

  table tr:nth-child(2n) {
    background-color: #f8f8f8;
  }

  table tr th {
    font-weight: bold;
    border: 1px solid #cccccc;
    text-align: left;
    margin: 0;
    padding: 6px 13px;
  }

  table tr td {
    border: 1px solid #cccccc;
    text-align: left;
    margin: 0;
    padding: 6px 13px;
  }

  table tr th :first-child, table tr td :first-child {
    margin-top: 0;
  }

  table tr th :last-child, table tr td :last-child {
    margin-bottom: 0;
  }

  img {
    max-width: 100%;
  }

  span.frame {
    display: block;
    overflow: hidden;
  }

  span.frame > span {
    border: 1px solid #dddddd;
    display: block;
    float: left;
    overflow: hidden;
    margin: 13px 0 0;
    padding: 7px;
    width: auto;
  }

  span.frame span img {
    display: block;
    float: left;
  }

  span.frame span span {
    clear: both;
    color: #333333;
    display: block;
    padding: 5px 0 0;
  }

  span.align-center {
    display: block;
    overflow: hidden;
    clear: both;
  }

  span.align-center > span {
    display: block;
    overflow: hidden;
    margin: 13px auto 0;
    text-align: center;
  }

  span.align-center span img {
    margin: 0 auto;
    text-align: center;
  }

  span.align-right {
    display: block;
    overflow: hidden;
    clear: both;
  }

  span.align-right > span {
    display: block;
    overflow: hidden;
    margin: 13px 0 0;
    text-align: right;
  }

  span.align-right span img {
    margin: 0;
    text-align: right;
  }

  span.float-left {
    display: block;
    margin-right: 13px;
    overflow: hidden;
    float: left;
  }

  span.float-left span {
    margin: 13px 0 0;
  }

  span.float-right {
    display: block;
    margin-left: 13px;
    overflow: hidden;
    float: right;
  }

  span.float-right > span {
    display: block;
    overflow: hidden;
    margin: 13px auto 0;
    text-align: right;
  }

  code, tt {
    margin: 0 2px;
    padding: 0 5px;
    white-space: nowrap;
    border: 1px solid #eaeaea;
    background-color: #f8f8f8;
    border-radius: 3px;
  }

  pre code {
    margin: 0;
    padding: 0;
    white-space: pre;
    border: none;
    background: transparent;
  }

  .highlight pre {
    background-color: #f8f8f8;
    border: 1px solid #cccccc;
    font-size: 13px;
    line-height: 19px;
    overflow: auto;
    padding: 6px 10px;
    border-radius: 3px;
  }

  pre {
    background-color: #f8f8f8;
    border: 1px solid #cccccc;
    font-size: 13px;
    line-height: 19px;
    overflow: auto;
    padding: 6px 10px;
    border-radius: 3px;
  }

  pre code, pre tt {
    background-color: transparent;
    border: none;
  }

"""

GITHUB_MARKDOWN_STRYLE_DARK="""
body {
  color-scheme: dark;
  -ms-text-size-adjust: 100%;
  -webkit-text-size-adjust: 100%;
  margin: 0;
  color: #c9d1d9;
  background-color: #0d1117;
  font-family: -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif,"Apple Color Emoji","Segoe UI Emoji";
  font-size: 16px;
  line-height: 1.5;
  word-wrap: break-word
}
body .octicon {
  display: inline-block;
  fill: currentColor;
  vertical-align: text-bottom
}
body h1:hover .anchor .octicon-link:before,
body h2:hover .anchor .octicon-link:before,
body h3:hover .anchor .octicon-link:before,
body h4:hover .anchor .octicon-link:before,
body h5:hover .anchor .octicon-link:before,
body h6:hover .anchor .octicon-link:before {
  width: 16px;
  height: 16px;
  content: ' ';
  display: inline-block;
  background-color: currentColor;
  -webkit-mask-image: url("data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16' version='1.1' aria-hidden='true'><path fill-rule='evenodd' d='M7.775 3.275a.75.75 0 001.06 1.06l1.25-1.25a2 2 0 112.83 2.83l-2.5 2.5a2 2 0 01-2.83 0 .75.75 0 00-1.06 1.06 3.5 3.5 0 004.95 0l2.5-2.5a3.5 3.5 0 00-4.95-4.95l-1.25 1.25zm-4.69 9.64a2 2 0 010-2.83l2.5-2.5a2 2 0 012.83 0 .75.75 0 001.06-1.06 3.5 3.5 0 00-4.95 0l-2.5 2.5a3.5 3.5 0 004.95 4.95l1.25-1.25a.75.75 0 00-1.06-1.06l-1.25 1.25a2 2 0 01-2.83 0z'></path></svg>");
  mask-image: url("data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16' version='1.1' aria-hidden='true'><path fill-rule='evenodd' d='M7.775 3.275a.75.75 0 001.06 1.06l1.25-1.25a2 2 0 112.83 2.83l-2.5 2.5a2 2 0 01-2.83 0 .75.75 0 00-1.06 1.06 3.5 3.5 0 004.95 0l2.5-2.5a3.5 3.5 0 00-4.95-4.95l-1.25 1.25zm-4.69 9.64a2 2 0 010-2.83l2.5-2.5a2 2 0 012.83 0 .75.75 0 001.06-1.06 3.5 3.5 0 00-4.95 0l-2.5 2.5a3.5 3.5 0 004.95 4.95l1.25-1.25a.75.75 0 00-1.06-1.06l-1.25 1.25a2 2 0 01-2.83 0z'></path></svg>")
}
body details,
body figcaption,
body figure {
  display: block
}
body summary {
  display: list-item
}
body a {
  background-color: transparent;
  color: #58a6ff;
  text-decoration: none
}
body a:active,
body a:hover {
  outline-width: 0
}
body abbr[title] {
  border-bottom: none;
  -webkit-text-decoration: underline dotted;
  text-decoration: underline dotted
}
body b,
body strong {
  font-weight: 600
}
body dfn {
  font-style: italic
}
body h1 {
  margin: .67em 0;
  font-weight: 600;
  padding-bottom: .3em;
  font-size: 2em;
  border-bottom: 1px solid #21262d
}
body mark {
  background-color: #ff0;
  color: #c9d1d9
}
body small {
  font-size: 90%
}
body sub,
body sup {
  font-size: 75%;
  line-height: 0;
  position: relative;
  vertical-align: baseline
}
body sub {
  bottom: -.25em
}
body sup {
  top: -.5em
}
body img {
  border-style: none;
  max-width: 100%;
  box-sizing: content-box;
  background-color: #0d1117
}
body code,
body kbd,
body pre,
body samp {
  font-family: monospace,monospace;
  font-size: 1em
}
body figure {
  margin: 1em 40px
}
body hr {
  box-sizing: content-box;
  overflow: hidden;
  background: 0 0;
  border-bottom: 1px solid #21262d;
  height: .25em;
  padding: 0;
  margin: 24px 0;
  background-color: #30363d;
  border: 0
}
body [type=reset],
body [type=submit],
body html [type=button] {
  -webkit-appearance: button
}
body [type=button]::-moz-focus-inner,
body [type=reset]::-moz-focus-inner,
body [type=submit]::-moz-focus-inner {
  border-style: none;
  padding: 0
}
body [type=button]:-moz-focusring,
body [type=reset]:-moz-focusring,
body [type=submit]:-moz-focusring {
  outline: 1px dotted ButtonText
}
body [type=checkbox],
body [type=radio] {
  box-sizing: border-box;
  padding: 0
}
body [type=number]::-webkit-inner-spin-button,
body [type=number]::-webkit-outer-spin-button {
  height: auto
}
body [type=search] {
  -webkit-appearance: textfield;
  outline-offset: -2px
}
body [type=search]::-webkit-search-cancel-button,
body [type=search]::-webkit-search-decoration {
  -webkit-appearance: none
}
body ::-webkit-input-placeholder {
  color: inherit;
  opacity: .54
}
body ::-webkit-file-upload-button {
  -webkit-appearance: button;
  font: inherit
}
body a:hover {
  text-decoration: underline
}
body hr::before {
  display: table;
  content: ""
}
body hr::after {
  display: table;
  clear: both;
  content: ""
}
body table {
  border-spacing: 0;
  border-collapse: collapse;
  display: block;
  width: max-content;
  max-width: 100%;
  overflow: auto
}
body td,
body th {
  padding: 0
}
body details summary {
  cursor: pointer
}
body details:not([open]) > :not(summary) {
  display: none!important
}
body kbd {
  display: inline-block;
  padding: 3px 5px;
  font: 11px ui-monospace,SFMono-Regular,SF Mono,Menlo,Consolas,Liberation Mono,monospace;
  line-height: 10px;
  color: #c9d1d9;
  vertical-align: middle;
  background-color: #161b22;
  border: solid 1px rgba(110,118,129,.4);
  border-bottom-color: rgba(110,118,129,.4);
  border-radius: 6px;
  box-shadow: inset 0 -1px 0 rgba(110,118,129,.4)
}
body h1,
body h2,
body h3,
body h4,
body h5,
body h6 {
  margin-top: 24px;
  margin-bottom: 16px;
  font-weight: 600;
  line-height: 1.25
}
body h2 {
  font-weight: 600;
  padding-bottom: .3em;
  font-size: 1.5em;
  border-bottom: 1px solid #21262d
}
body h3 {
  font-weight: 600;
  font-size: 1.25em
}
body h4 {
  font-weight: 600;
  font-size: 1em
}
body h5 {
  font-weight: 600;
  font-size: .875em
}
body h6 {
  font-weight: 600;
  font-size: .85em;
  color: #8b949e
}
body p {
  margin-top: 0;
  margin-bottom: 10px
}
body blockquote {
  margin: 0;
  padding: 0 1em;
  color: #8b949e;
  border-left: .25em solid #30363d
}
body ol,
body ul {
  margin-top: 0;
  margin-bottom: 0;
  padding-left: 2em
}
body ol ol,
body ul ol {
  list-style-type: lower-roman
}
body ol ol ol,
body ol ul ol,
body ul ol ol,
body ul ul ol {
  list-style-type: lower-alpha
}
body dd {
  margin-left: 0
}
body code,
body tt {
  font-family: ui-monospace,SFMono-Regular,SF Mono,Menlo,Consolas,Liberation Mono,monospace;
  font-size: 12px
}
body pre {
  margin-top: 0;
  margin-bottom: 0;
  font-family: ui-monospace,SFMono-Regular,SF Mono,Menlo,Consolas,Liberation Mono,monospace;
  font-size: 12px;
  word-wrap: normal
}
body :-ms-input-placeholder {
  color: #484f58;
  opacity: 1
}
body ::-ms-input-placeholder {
  color: #484f58;
  opacity: 1
}
body ::placeholder {
  color: #484f58;
  opacity: 1
}
body .pl-c {
  color: #8b949e
}
body .pl-c1,
body .pl-s .pl-v {
  color: #79c0ff
}
body .pl-e,
body .pl-en {
  color: #d2a8ff
}
body .pl-s .pl-s1,
body .pl-smi {
  color: #c9d1d9
}
body .pl-ent {
  color: #7ee787
}
body .pl-k {
  color: #ff7b72
}
body .pl-pds,
body .pl-s,
body .pl-s .pl-pse .pl-s1,
body .pl-sr,
body .pl-sr .pl-cce,
body .pl-sr .pl-sra,
body .pl-sr .pl-sre {
  color: #a5d6ff
}
body .pl-smw,
body .pl-v {
  color: #ffa657
}
body .pl-bu {
  color: #f85149
}
body .pl-ii {
  color: #f0f6fc;
  background-color: #8e1519
}
body .pl-c2 {
  color: #f0f6fc;
  background-color: #b62324
}
body .pl-sr .pl-cce {
  font-weight: 700;
  color: #7ee787
}
body .pl-ml {
  color: #f2cc60
}
body .pl-mh,
body .pl-mh .pl-en,
body .pl-ms {
  font-weight: 700;
  color: #1f6feb
}
body .pl-mi {
  font-style: italic;
  color: #c9d1d9
}
body .pl-mb {
  font-weight: 700;
  color: #c9d1d9
}
body .pl-md {
  color: #ffdcd7;
  background-color: #67060c
}
body .pl-mi1 {
  color: #aff5b4;
  background-color: #033a16
}
body .pl-mc {
  color: #ffdfb6;
  background-color: #5a1e02
}
body .pl-mi2 {
  color: #c9d1d9;
  background-color: #1158c7
}
body .pl-mdr {
  font-weight: 700;
  color: #d2a8ff
}
body .pl-ba {
  color: #8b949e
}
body .pl-sg {
  color: #484f58
}
body .pl-corl {
  text-decoration: underline;
  color: #a5d6ff
}
body [data-catalyst] {
  display: block
}
body g-emoji {
  font-family: "Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol";
  font-size: 1em;
  font-style: normal!important;
  font-weight: 400;
  line-height: 1;
  vertical-align: -.075em
}
body g-emoji img {
  width: 1em;
  height: 1em
}
body::before {
  display: table;
  content: ""
}
body::after {
  display: table;
  clear: both;
  content: ""
}
body > :first-child {
  margin-top: 0!important
}
body > :last-child {
  margin-bottom: 0!important
}
body a:not([href]) {
  color: inherit;
  text-decoration: none
}
body .absent {
  color: #f85149
}
body .anchor {
  float: left;
  padding-right: 4px;
  margin-left: -20px;
  line-height: 1
}
body .anchor:focus {
  outline: 0
}
body blockquote,
body details,
body dl,
body ol,
body p,
body pre,
body table,
body ul {
  margin-top: 0;
  margin-bottom: 16px
}
body blockquote > :first-child {
  margin-top: 0
}
body blockquote > :last-child {
  margin-bottom: 0
}
body sup > a::before {
  content: "["
}
body sup > a::after {
  content: "]"
}
body h1 .octicon-link,
body h2 .octicon-link,
body h3 .octicon-link,
body h4 .octicon-link,
body h5 .octicon-link,
body h6 .octicon-link {
  color: #c9d1d9;
  vertical-align: middle;
  visibility: hidden
}
body h1:hover .anchor,
body h2:hover .anchor,
body h3:hover .anchor,
body h4:hover .anchor,
body h5:hover .anchor,
body h6:hover .anchor {
  text-decoration: none
}
body h1:hover .anchor .octicon-link,
body h2:hover .anchor .octicon-link,
body h3:hover .anchor .octicon-link,
body h4:hover .anchor .octicon-link,
body h5:hover .anchor .octicon-link,
body h6:hover .anchor .octicon-link {
  visibility: visible
}
body h1 code,
body h1 tt,
body h2 code,
body h2 tt,
body h3 code,
body h3 tt,
body h4 code,
body h4 tt,
body h5 code,
body h5 tt,
body h6 code,
body h6 tt {
  padding: 0 .2em;
  font-size: inherit
}
body ol.no-list,
body ul.no-list {
  padding: 0;
  list-style-type: none
}
body ol[type="1"] {
  list-style-type: decimal
}
body ol[type=a] {
  list-style-type: lower-alpha
}
body ol[type=i] {
  list-style-type: lower-roman
}
body div > ol:not([type]) {
  list-style-type: decimal
}
body ol ol,
body ol ul,
body ul ol,
body ul ul {
  margin-top: 0;
  margin-bottom: 0
}
body li > p {
  margin-top: 16px
}
body li + li {
  margin-top: .25em
}
body dl {
  padding: 0
}
body dl dt {
  padding: 0;
  margin-top: 16px;
  font-size: 1em;
  font-style: italic;
  font-weight: 600
}
body dl dd {
  padding: 0 16px;
  margin-bottom: 16px
}
body table th {
  font-weight: 600
}
body table td,
body table th {
  padding: 6px 13px;
  border: 1px solid #30363d
}
body table tr {
  background-color: #0d1117;
  border-top: 1px solid #21262d
}
body table tr:nth-child(2n) {
  background-color: #161b22
}
body table img {
  background-color: transparent
}
body img[align=right] {
  padding-left: 20px
}
body img[align=left] {
  padding-right: 20px
}
body .emoji {
  max-width: none;
  vertical-align: text-top;
  background-color: transparent
}
body span.frame {
  display: block;
  overflow: hidden
}
body span.frame > span {
  display: block;
  float: left;
  width: auto;
  padding: 7px;
  margin: 13px 0 0;
  overflow: hidden;
  border: 1px solid #30363d
}
body span.frame span img {
  display: block;
  float: left
}
body span.frame span span {
  display: block;
  padding: 5px 0 0;
  clear: both;
  color: #c9d1d9
}
body span.align-center {
  display: block;
  overflow: hidden;
  clear: both
}
body span.align-center > span {
  display: block;
  margin: 13px auto 0;
  overflow: hidden;
  text-align: center
}
body span.align-center span img {
  margin: 0 auto;
  text-align: center
}
body span.align-right {
  display: block;
  overflow: hidden;
  clear: both
}
body span.align-right > span {
  display: block;
  margin: 13px 0 0;
  overflow: hidden;
  text-align: right
}
body span.align-right span img {
  margin: 0;
  text-align: right
}
body span.float-left {
  display: block;
  float: left;
  margin-right: 13px;
  overflow: hidden
}
body span.float-left span {
  margin: 13px 0 0
}
body span.float-right {
  display: block;
  float: right;
  margin-left: 13px;
  overflow: hidden
}
body span.float-right > span {
  display: block;
  margin: 13px auto 0;
  overflow: hidden;
  text-align: right
}
body code,
body tt {
  padding: .2em .4em;
  margin: 0;
  font-size: 85%;
  background-color: rgba(110,118,129,.4);
  border-radius: 6px
}
body code br,
body tt br {
  display: none
}
body del code {
  text-decoration: inherit
}
body pre code {
  font-size: 100%
}
body pre > code {
  padding: 0;
  margin: 0;
  word-break: normal;
  white-space: pre;
  background: 0 0;
  border: 0
}
body .highlight {
  margin-bottom: 16px
}
body .highlight pre {
  margin-bottom: 0;
  word-break: normal
}
body .highlight pre,
body pre {
  padding: 16px;
  overflow: auto;
  font-size: 85%;
  line-height: 1.45;
  background-color: #161b22;
  border-radius: 6px
}
body pre code,
body pre tt {
  display: inline;
  max-width: auto;
  padding: 0;
  margin: 0;
  overflow: visible;
  line-height: inherit;
  word-wrap: normal;
  background-color: transparent;
  border: 0
}
body .csv-data td,
body .csv-data th {
  padding: 5px;
  overflow: hidden;
  font-size: 12px;
  line-height: 1;
  text-align: left;
  white-space: nowrap
}
body .csv-data .blob-num {
  padding: 10px 8px 9px;
  text-align: right;
  background: #0d1117;
  border: 0
}
body .csv-data tr {
  border-top: 0
}
body .csv-data th {
  font-weight: 600;
  background: #161b22;
  border-top: 0
}
body .footnotes {
  font-size: 12px;
  color: #8b949e;
  border-top: 1px solid #30363d
}
body .footnotes ol {
  padding-left: 16px
}
body .footnotes li {
  position: relative
}
body .footnotes li:target::before {
  position: absolute;
  top: -8px;
  right: -8px;
  bottom: -8px;
  left: -24px;
  pointer-events: none;
  content: "";
  border: 2px solid #1f6feb;
  border-radius: 6px
}
body .footnotes li:target {
  color: #c9d1d9
}
body .footnotes .data-footnote-backref g-emoji {
  font-family: monospace
}
body [hidden] {
  display: none!important
}
body ::-webkit-calendar-picker-indicator {
  filter: invert(50%)
}
"""