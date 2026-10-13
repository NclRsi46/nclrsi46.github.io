---
layout: page
title: Experience
permalink: /resume.html
description: "Nicolas Rossi's experience: Corveonic, Pace ITS, cybersecurity competitions, education, and skills."
lede: "Work, competitions, and education, in the same words as my resume."
kv:
  - label: Resume
    from: resume
    link: Resume (PDF)
  - label: Languages
    from: languages
---
{% comment %}Copy approved by Nick 2026-10-12 (Session B). Entries: _data/experience.yml.{% endcomment %}
{%- assign x = site.data.experience %}

<section aria-labelledby="work">
  {% include sec-head.html n="01" id="work" title="Work" %}
  {% include entries.html items=x.work %}
</section>

<section aria-labelledby="comp">
  {% include sec-head.html n="02" id="comp" title="Competitions" %}
  {% include entries.html items=x.competitions %}
</section>

<section aria-labelledby="edu">
  {% include sec-head.html n="03" id="edu" title="Education" %}
  {% include entries.html items=x.education %}
</section>

<section aria-labelledby="proj">
  {% include sec-head.html n="04" id="proj" title="Projects" %}
  {% include entries.html items=x.projects %}
</section>

<section aria-labelledby="skills">
  {% include sec-head.html n="05" id="skills" title="Skills" %}
  <dl class="rows">
    {%- for s in x.skills %}
    <div><dt>{{ s.group | escape }}</dt><dd>{{ s.items | escape }}</dd></div>
    {%- endfor %}
  </dl>
</section>

<section aria-labelledby="orgs">
  {% include sec-head.html n="06" id="orgs" title="Organizations" %}
  {% include entries.html items=x.organizations %}
</section>
