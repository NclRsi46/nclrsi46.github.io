---
layout: page
title: Phishing Domain Classifier
label: Case study
permalink: /projects/phishing-domain-classifier/
description: "Case study: a phishing domain classifier whose 99.46% accuracy was a data leak, and how Nicolas Rossi rebuilt its evaluation."
lede: "A team course project at Pace in fall 2025, where I wrote the implementation. Its first result, 99.46% accuracy, came from a data leak."
kv:
  - label: Stack
    value: Python, scikit-learn
  - label: Code
    value: https://github.com/NclRsi46/phishing-detection-ml
    link: GitHub repository
---
{% comment %}Copy approved by Nick 2026-10-12 (Session B), lines K1–K22 in _prototypes/copy.md.
Every number: phishing-detection-ml README.md at 4b5abc1 and results/repeated_splits.json.{% endcomment %}

<section aria-labelledby="first" markdown="1">
{% include sec-head.html n="01" id="first" title="The first version" %}
<div class="prose" markdown="1">
The first version scored full URLs with a Random Forest and reported 99.46% accuracy, 99.80% precision, and a 0.20% false positive rate on held-out data.

None of it meant anything. Every benign example was a popular domain from the Tranco list with https:// in front of it, a bare homepage, while 97.0% of the phishing URLs from PhishTank had something after the host. The model learned that anything after the domain means phishing: the slash count alone carried 60% of its feature importance. It gave en.wikipedia.org/wiki/Phishing a phishing score of 1.00 and paypal-login-secure.com 0.11.

The split leaked too. PhishTank often lists many URLs on one domain, so the same domain landed in both train and test, and the evaluation script scored the model on the full dataset, training rows included.
</div>
</section>

<section aria-labelledby="rebuild" markdown="1">
{% include sec-head.html n="02" id="rebuild" title="Rebuilding the evaluation" %}
<div class="prose" markdown="1">
I rebuilt the pipeline to score the domain name only, discarding the path, query, and scheme. The same leak showed up one level down: Tranco lists no subdomains, while 84% of PhishTank hostnames have one, so the main experiment scores the registered domain alone.

The train/test split is grouped by phishing campaign. Domains that differ only by a number or the TLD, like pl-oferta48213.sbs and pl-oferta77120.cfd, always land on the same side. Every result is a mean and standard deviation over 10 grouped splits, so one lucky split can't carry it.

At the default 0.5 threshold the false positive rate is above 20%, far too high to block anything. So I report recall at a fixed false positive rate: the share of phishing caught at the best threshold that flags no more than 1% of benign domains.
</div>
</section>

<section aria-labelledby="results">
  {% include sec-head.html n="03" id="results" title="Results" %}
  <dl class="rows">
    <div><dt>Hand-built features</dt><dd>Logistic Regression: 13.7% ± 4.3 recall at 1% FPR · 72.6% average precision</dd></div>
    <div><dt>Hand-built features</dt><dd>Random Forest: 12.7% ± 7.9 recall at 1% FPR · 71.5% average precision</dd></div>
    <div><dt>Character n-grams</dt><dd>Logistic Regression: 27.7% ± 4.8 recall at 1% FPR · 79.6% average precision</dd></div>
  </dl>
  <div class="prose">
    <p>Domain level, mean ± standard deviation over the 10 splits. Most of the forest’s ± 7.9 comes from two splits where tied top scores leave no threshold under 1%. On full hostnames the n-gram model reaches 32.7% ± 3.2.</p>
    <p>The threshold is read off each test split’s ROC curve, so recall at 1% FPR measures how well a model ranks domains, not a threshold you could deploy. A threshold picked on one split won’t land at exactly 1% on new data.</p>
  </div>
</section>

<section aria-labelledby="gain" markdown="1">
{% include sec-head.html n="04" id="gain" title="Where the gain came from" %}
<div class="prose" markdown="1">
The n-gram model roughly doubles recall at 1% FPR, but much of that gain isn't new knowledge about how phishing names look.

The hand-built features sort TLDs into four groups, so .cfd, .icu, and .sbs look the same to them. Adding the full suffix takes their recall at 1% FPR from 13.7% to 19.4%, about 40% of the way to the n-gram model.

Much of the rest is phishing-kit wording, like pl-oferta and coursier, that repeats across campaigns. On test names that share no 8-character substring with a training phishing name, recall at 1% FPR falls to 1.7–3.9% for the hand-feature models and 12.6% for the n-gram model.
</div>
</section>

<section aria-labelledby="limits" markdown="1">
{% include sec-head.html n="05" id="limits" title="Limits and the lesson" %}
<div class="prose" markdown="1">
Used honestly, this is a narrow high-confidence signal for triage, not a filter. Domain-only features can't see phishing on a compromised legitimate site, the benign lists measure popularity rather than safety, and lexical models decay as attackers change names and TLDs. A two-week time-based split was a first look at that, not an answer.

When two classes come from different sources, check every column for differences in how the data was collected before trusting any score. A near-perfect result on a hard problem is a reason to look for leakage, not to celebrate.
</div>
</section>
