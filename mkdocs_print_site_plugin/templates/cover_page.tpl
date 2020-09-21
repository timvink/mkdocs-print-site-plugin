
<div style="padding-bottom: 3em">

    {% if config.site_description %}
        <h1>{{ config.site_name }}</h1>
    {% endif %}

    {% if config.site_description %}
        <h2>{{ config.site_description }}</h2>
    {% endif %}

</div>

{% if config.site_author %}
    <p>Authors: {{ config.site_author }}</p>
{% endif %}

<p>
    {% if config.site_url %}
        <small>Website: <a href="{{ config.site_url }}">{{ config.site_url }}</a></small><br />
    {% endif %}
    {% if config.repo_url %}
        <small>Repo: <a href="{{ config.repo_url }}">{{ config.repo_url }}</a></small><br />
    {% endif %}
    {% if config.copyright %}
        <small>{{ config.copyright }}</small><br />
    {% endif %}
</p>
