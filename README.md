# nclrsi46.github.io

Personal site of Nicolas Rossi, cybersecurity student at Pace University.

Live at https://nclrsi46.github.io. GitHub Pages builds it with Jekyll from `main`.

## Local build

Needs Ruby 3.3 to match the Pages builder (`brew install ruby@3.3`), then:

```sh
/opt/homebrew/opt/ruby@3.3/bin/bundle config set --local path vendor/bundle
/opt/homebrew/opt/ruby@3.3/bin/bundle install
script/build
```

`script/build` runs the `github-pages` executable the way the Pages action does. Plain `jekyll build` skips the Pages plugins and overrides, so its output can differ from production.
