tinymce.init({
  selector: 'textarea',  // change this value according to your HTML
  menu: {
    edit: {title: 'Edit', items: 'undo redo | cut copy paste pastetext | selectall'},
    insert: {title: 'Insert', items: 'link media | template hr'},
    format: {title: 'Format', items: 'bold italic underline strikethrough superscript subscript | formats | removeformat'},
    tools: {title: 'Tools', items: 'spellchecker code'}
  }
});

