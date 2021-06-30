import htmlgenerator as hg

from bread.layout.components import search

from .tag import Tag


class SearchSelect(hg.DIV):
    def __init__(
        self,
        backend,
        boundfield,
        widgetattributes,
        **elementattributes,
    ):
        """
        :param SearchBackendConfig backend: Where and how to get search results
        """

        widgetattributes["value"] = widgetattributes["value"][0]
        # This works inside a formset. Might need to be changed for other usages.
        current_selection = getattr(
            boundfield.form.instance, elementattributes["fieldname"], ""
        )

        resultcontainerid = f"search-result-{widgetattributes['id']}"
        widget_id = widgetattributes["id"]
        tag_id = f"{widget_id}-tag"
        super().__init__(
            Tag(
                current_selection,
                id=tag_id,
                style=hg.If(
                    widgetattributes["value"] == "",
                    hg.BaseElement("visibility: hidden"),
                ),
                onclick="return false;",
            ),
            hg.INPUT(_type="hidden", **widgetattributes),  # the actual form field
            search.Search(
                backend=backend,
                resultcontainerid=resultcontainerid,
                resultcontainer_onload_js=_resultcontainer_onload_js(
                    backend, resultcontainerid, tag_id, widget_id
                ),
                size="lg",
                disabled=widgetattributes.get("disabled", False),
            ),
            style="display: flex;",
            **elementattributes,
        )


def _resultcontainer_onload_js(backend, resultcontainerid, tag_id, widget_id):
    on_click = f"""function(evt) {{
        let label = $('{backend.result_label_selector}', this).innerHTML;
        let value = $('{backend.result_value_selector}', this).innerHTML;
        $('#{widget_id}').value = value;
        $('#{tag_id}').innerHTML = label;
        $('#{tag_id}').style = 'visiblity: visible';
        }}"""

    return f"""
    document.addEventListener('click', (evt) => this.innerHTML='');
    htmx.onLoad(function(target) {{
    $$('#{resultcontainerid} {backend.result_selector}')._
    .addEventListener('click', {on_click});
    }});"""
