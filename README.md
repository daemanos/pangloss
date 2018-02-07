# pangloss

Provides support for interlinear glosses with Markdown example lists.

## Example

The following code snippet demonstrates the most important features of
pangloss:

```
As you can see in the following examples, pangloss is really easy to use:

(@) Jorge  llama             a  Maria.
    George calls-3s.PRES.IND to Maria
    'George calls Maria.'
(@) Aussi, vous pouvez          avoir    de multiples   exemples.
    also   you  can-2p.PRES.IND have.INF of multiple-PL example-PL
    'You can also have multiple examples.' {#ex:french}

You can even refer to examples, as in @ex:french.
```

Each example consists of three lines: an original, a word-by-word analysis, and
an overall translation. Placing `{#ex:...}` after the translation line
introduces a new label, which can then be referred to with the `@ex:...`
syntax as in [pandoc-crossref](https://github.com/lierdakil/pandoc-crossref).
Similar customization of labels and more advanced references are coming soon.

## Installation

Install with:

```
pip install -U pangloss
```

Use with:

```
pandoc in.md -F pangloss -o out.{pdf,html}
```
