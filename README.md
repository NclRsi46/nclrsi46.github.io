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

`script/build` runs the `github-pages` executable the way the Pages action does: Ruby 3.3, UTF-8 locale, `JEKYLL_ENV=production`. The gem sits in the `:jekyll_plugins` group, so plain `bundle exec jekyll build` and `jekyll serve` also load the Pages configuration (safe mode, forced plugins, theme default), but they skip the locale and production env, so verify with `script/build`.

## Social card

`assets/img/og-card.png` (1200×630) is rendered from `script/og-card.html` by `script/og-card` with headless Chrome. Rerun it after changing the name or tagline.
