# coding: utf-8
from django import forms
from django.core.urlresolvers import reverse
from crispy_forms.helper import FormHelper
from crispy_forms_foundation.layout import Layout, Row, Column, Fieldset, Field, HTML, Submit
from django.conf import settings


class NewListAjaxForm(forms.Form):
    title = forms.CharField(label='Title', max_length=80)
    description = forms.CharField(
        label='Description', required=False, widget=forms.Textarea())
    private = forms.BooleanField(label='private', required=False)

    # display a select with languages ordered by most used first
    from resrc.language.models import Language
    from django.db.models import Count
    used_langs = Language.objects.all().annotate(
        c=Count('link')).order_by('-c').values_list()
    used_langs = [x[1] for x in used_langs]
    lang_choices = []
    for lang in used_langs:
        lang_choices += [x for x in settings.LANGUAGES if x[0] == lang]
    lang_choices += [x for x in settings.LANGUAGES if x not in lang_choices]

    language = forms.ChoiceField(label='Language', choices=lang_choices)

    def __init__(self, link_pk, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_id = 'createlistform'
        self.helper.form_action = reverse('ajax-create-list', args=(link_pk,))

        self.helper.layout = Layout(
            Fieldset(
                u'Create a list',
                Row(
                    Column(
                        Field('title'), css_class='large-12'
                    ),
                ),
                Row(
                    Column(
                        Field('description'), css_class='large-12'
                    ),
                ),
                Row(
                    Column(
                        Field('private'), css_class='large-4'
                    ),
                    Column(
                        Field('language'), css_class='large-4'
                    ),
                ),
            ),
            Row(
                Column(
                    HTML('<a id="createlist" class="small button">Create</a><a id="createclose" class="small secondary button" style="display:none">Close</a>'), css_class='large-12'
                ),
            ),
        )
        super(NewListAjaxForm, self).__init__(*args, **kwargs)


class NewListForm(forms.Form):
    title = forms.CharField(label='Title', max_length=80)
    description = forms.CharField(
        label='Description', required=False, widget=forms.Textarea()
    )
    url = forms.URLField(
        label='URL', required=False
    )
    private = forms.BooleanField(label='private', required=False)
    mdcontent = forms.CharField(
        label='content', required=False, widget=forms.Textarea()
    )

    # display a select with languages ordered by most used first
    from resrc.language.models import Language
    from django.db.models import Count
    used_langs = Language.objects.all().annotate(
        c=Count('link')).order_by('-c').values_list()
    used_langs = [x[1] for x in used_langs]
    lang_choices = []
    for lang in used_langs:
        lang_choices += [x for x in settings.LANGUAGES if x[0] == lang]
    lang_choices += [x for x in settings.LANGUAGES if x not in lang_choices]

    language = forms.ChoiceField(label='Language', choices=lang_choices)

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_id = 'createlistform'

        self.helper.layout = Layout(
            Fieldset(
                u'Create a list',
                Row(
                    Column(
                        Field('title'), css_class='large-12'
                    ),
                ),
                Row(
                    Column(
                        Field('description'), css_class='large-12'
                    ),
                ),
                Row(
                    Column(
                        Field('url'), css_class='large-12'
                    ),
                ),
                Row(
                    Column(
                        HTML('<label for="id_private"><input class="checkboxinput" id="id_private" name="private" type="checkbox"> private</label>'),
                        css_class='large-6'
                    ),
                    Column(
                        Field('language'),
                        css_class='large-6'
                    ),
                ),
                Row(
                    Column(
                        Field('mdcontent'),
                        css_class='large-12'
                    ),
                    css_class='markdownform'
                ),
            ),
            Row(
                Column(
                    Submit('submit', 'Save', css_class='small button'),
                    css_class='large-12',
                ),
            )
        )
        super(NewListForm, self).__init__(*args, **kwargs)


class EditListForm(forms.Form):
    title = forms.CharField(label='Title', max_length=80)
    description = forms.CharField(
        label='Description', required=False, widget=forms.Textarea()
    )
    url = forms.URLField(
        label='URL', required=False
    )
    private = forms.BooleanField(label='private', required=False)
    mdcontent = forms.CharField(
        label='list source', required=False, widget=forms.Textarea()
    )

    # display a select with languages ordered by most used first
    from resrc.language.models import Language
    from django.db.models import Count
    used_langs = Language.objects.all().annotate(
        c=Count('link')).order_by('-c').values_list()
    used_langs = [x[1] for x in used_langs]
    lang_choices = []
    for lang in used_langs:
        lang_choices += [x for x in settings.LANGUAGES if x[0] == lang]
    lang_choices += [x for x in settings.LANGUAGES if x not in lang_choices]

    language = forms.ChoiceField(label='Language', choices=lang_choices)

    def __init__(self, private_checkbox, alist, from_url, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_id = 'createlistform'

        delete_url = reverse('list-delete', args=(alist.pk,))

        if not from_url:
            self.helper.layout = Layout(
                Fieldset(
                    u'Edit a list',
                    Row(
                        Column(
                            Field('title'), css_class='large-12'
                        ),
                    ),
                    Row(
                        Column(
                            Field('description'), css_class='large-12'
                        ),
                    ),
                    Row(
                        Column(
                            Field('url'), css_class='large-12'
                        ),
                    ),
                    Row(
                        Column(
                            HTML('<label for="id_private"><input class="checkboxinput" id="id_private" name="private" type="checkbox" %s> private</label>' % private_checkbox),
                            css_class='large-6'
                        ),
                        Column(
                            Field('language'),
                            css_class='large-6'
                        ),
                    ),
                    Row(
                        Column(
                            Field('mdcontent'),
                            css_class='large-12'
                        ),
                        css_class='markdownform'
                    ),
                ),
                Row(
                    Column(
                        Submit('submit', 'Save', css_class='small button'),
                        css_class='large-6',
                    ),
                    Column(
                        HTML('<a href="%s" class="small button alert right" data-id="%s">Delete list</a>' % (delete_url, alist.pk)),
                        css_class='large-6'
                    ),
                )
            )
        else:
            self.helper.layout = Layout(
                Fieldset(
                    u'Edit a list',
                    Row(
                        Column(
                            Field('title'), css_class='large-12'
                        ),
                    ),
                    Row(
                        Column(
                            Field('description'), css_class='large-12'
                        ),
                    ),
                    Row(
                        Column(
                            Field('url'), css_class='large-12'
                        ),
                    ),
                    Row(
                        Column(
                            HTML('<label for="id_private"><input class="checkboxinput" id="id_private" name="private" type="checkbox" %s> private</label>' % private_checkbox),
                            css_class='large-6'
                        ),
                        Column(
                            Field('language'),
                            css_class='large-6'
                        ),
                    ),
                ),
                Row(
                    Column(
                        Submit('submit', 'Fetch and save', css_class='small button'),
                        css_class='large-12',
                    ),
                )
            )

        super(EditListForm, self).__init__(*args, **kwargs)
