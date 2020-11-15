from bread.utils import pretty_fieldname, pretty_modelname

import plisplate
from plisplate import *  # noqa

from . import button, datatable, form, grid, icon, notification  # noqa


class ModelContext(plisplate.ValueProvider):
    """Provides a model to marked child elements"""

    attributename = "model"

    def __init__(self, model, *children):
        super().__init__(model, *children)


class ObjectContext(plisplate.ValueProvider):
    """Provides a model instance to marked child elements """

    attributename = "object"

    def __init__(self, object, *children):
        super().__init__(object, *children)


class ModelFieldLabel(ModelContext.ConsumerMixin(), ObjectContext.ConsumerMixin()):
    def __init__(self, fieldname):
        self.fieldname = fieldname

    def render(self, context):
        if not hasattr(self, "model") and hasattr(self, "object"):
            self.model = self.object
        yield pretty_fieldname(self.model._meta.get_field(self.fieldname))

    def __repr__(self):
        return f"ModelFieldLabel({self.fieldname})"


class ModelName(ModelContext.ConsumerMixin(), ObjectContext.ConsumerMixin()):
    def __init__(self, plural=False):
        self.plural = plural

    def render(self, context):
        if not hasattr(self, "model") and hasattr(self, "object"):
            self.model = self.object
        yield pretty_modelname(self.model._meta.get_field(self.fieldname), self.plural)

    def __repr__(self):
        return f"ModelName({self.fieldname})"


class ModelFieldValue(ObjectContext.ConsumerMixin()):
    def __init__(self, fieldname):
        self.fieldname = fieldname

    def render(self, context):
        yield from self._try_render(getattr(self.object, self.fieldname, None), context)

    def __repr__(self):
        return f"ModelFieldValue({self.fieldname})"
