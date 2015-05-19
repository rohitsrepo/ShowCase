var ImageExtension;

function copyInto(dest, source, overwrite) {
    "use strict";
    var prop;
    dest = dest || {};
    for (prop in source) {
        if (source.hasOwnProperty(prop) && (overwrite || dest.hasOwnProperty(prop) === false)) {
            dest[prop] = source[prop];
        }
    }
    return dest;
}

function derives(base, derived) {
    "use strict";
    var origPrototype = derived.prototype;
    function Proto() { }
    Proto.prototype = base.prototype;
    derived.prototype = new Proto();
    derived.prototype.constructor = base;
    derived.prototype = copyInto(derived.prototype, origPrototype);
    return derived;
}

/*jslint plusplus: true */
function TableDerived(options) {
    "use strict";
    this.parent = true;
    this.hasForm = true;
    this.options = copyInto({
        name: 'image',
        action: 'insertImage',
        aria: 'image',
        tagNames: ['img'],
        contentDefault: '<b>IM</b>',
        contentFA: '<i class="fa fa-picture-o"></i>'
    }, options || {}, true);
}

TableDerived.prototype = {

    // Called when the button the toolbar is clicked
    // Overrides DefaultButton.handleClick
    handleClick: function (evt) {
        evt.preventDefault();
        evt.stopPropagation();

        if (!this.isDisplayed()) {
            this.showForm();
        }

        return false;
    },

    hideForm: function () {
        this.getForm().style.display = 'none';
    },

    showForm: function () {
        this.base.saveSelection();
        this.base.hideToolbarDefaultActions();
        var form = this.getForm();
        form.style.display = 'block';
        document.getElementsByTagName("body")[0].appendChild(form);
        this.base.setToolbarPosition();
    },

    createForm: function () {

        var doc=this.base.options.ownerDocument,
            addImage = document.createElement('section'),
            box = document.createElement('div'),
            crop = document.createElement('section'),
            cropHeader = document.createElement('h3'),
            upload = document.createElement('section'),
            uploadHeader = document.createElement('h3'),
            inputFile = document.createElement('input');

            addImage.className = 'add-image';
            box.className = 'small-box';
            crop.className = 'crop-image';
            upload.className = 'upload-image';
            inputFile.className = 'file';

            cropHeader.innerText = 'Crop Painting';
            uploadHeader.innerText = 'Upload Image';

            crop.appendChild(cropHeader);
            upload.appendChild(uploadHeader);

            inputFile.setAttribute('type', 'file');
            this.base.on(inputFile, 'change', this.handleUploadPainting.bind(this), true);
            upload.appendChild(inputFile);

            box.appendChild(crop);
            box.appendChild(upload);

            addImage.appendChild(box);
            addImage.style.display = 'none';

            return addImage;
    },

    createForm1: function () {
        var doc = this.base.options.ownerDocument,
            form = doc.createElement('section'),
            close = doc.createElement('a'),
            save = doc.createElement('a');
            // columnInput = doc.createElement('input'),
            // rowInput = doc.createElement('input');

        form.className = 'medium-editor-toolbar-form';
        form.id = 'medium-editor-toolbar-form-table-' + this.base.id;

        // Handle clicks on the form itself
        this.base.on(form, 'click', this.handleFormClick.bind(this));

        // Add save buton
        save.setAttribute('href', '#');
        save.className = 'medium-editor-toolbar-save';
        // save.innerHTML = this.base.options.buttonLabels === 'fontawesome' ?
        //                  '<i class="fa fa-check"></i>' :
        //                  '&#10003;';
        save.innerHTML = 'Crop Painting'
        form.appendChild(save);

        // Handle save button clicks (capture)
        this.base.on(save, 'click', this.handleCropPainting.bind(this), true);

        // Add close button
        close.setAttribute('href', '#');
        close.className = 'medium-editor-toolbar-close';
        // close.innerHTML = this.base.options.buttonLabels === 'fontawesome' ?
        //                   '<i class="fa fa-times"></i>' :
        //                   '&times;';
        close.innerHTML = 'Upload File'
        form.appendChild(close);

        // Handle close button clicks
        this.base.on(close, 'click', this.handleUploadPainting.bind(this));

        return form;
    },

    handleCropPainting: function (evt) {
        evt.preventDefault();
        evt.stopPropagation();

        url = 'http://c300221.r21.cf1.rackcdn.com/the-paintings-of-vicente-romero-redondo-lovely-women-in-hot-weather-boy-with-a-hat-1381023779_b.jpg';
        this.doImageSave(url);
    },

    handleUploadPainting : function (evt) {
        evt.preventDefault();
        evt.stopPropagation();

        file = evt.target.files[0];
        console.log("got file", file);
        url = 'http://www.daydaypaint.com/images/Pino/Pino-Painting-009.jpg';
        this.doImageSave(url);
    },

    createImageHtml : function (url) {
         var doc = this.base.options.ownerDocument,
         img = doc.createElement('img')
         ,wrap = doc.createElement('div');

         img.setAttribute('src', url);

         wrap.appendChild(img)
         return wrap;
    },

    doImageSave : function (url) {
         var doc = this.base.options.ownerDocument;

        doc.execCommand('insertImage', false, url);
    }
}

ImageExtension = derives(MediumEditor.statics.AnchorExtension, TableDerived);
