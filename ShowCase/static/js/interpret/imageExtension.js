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
function ImageDerived(options) {
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

ImageDerived.prototype = {

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

    handleCropPainting: function (evt) {
        evt.preventDefault();
        evt.stopPropagation();

        url = 'http://c300221.r21.cf1.rackcdn.com/the-paintings-of-vicente-romero-redondo-lovely-women-in-hot-weather-boy-with-a-hat-1381023779_b.jpg';
        this.doImageSave(url);
    },

    handleDeletePainting: function (evt) {
        this.options.scope.deleteFile(evt.toElement.id).then(function () {
            evt.toElement.parentElement.remove();
        });
    },

    handleUploadPainting : function (evt) {
        evt.preventDefault();
        evt.stopPropagation();

        file = evt.target.files[0];
        var that = this;
        this.options.scope.uploadFile(file).then(function (data) {
            that.doImageSave(data);
        });
    },

    createImageHtml : function (data) {
        var doc = this.base.options.ownerDocument,
        img = doc.createElement('img'),
        container = doc.createElement('section'),
        actions = doc.createElement('section'),
        wrap = doc.createElement('div');

        container.className = 'image-holder';

        actions.className = 'image-actions';
        actions.innerText = 'Remove';
        actions.id = data.id;
        actions.setAttribute('ng-click', "deleteFile('"+data.id+"')");

        this.base.on(actions, 'click', this.handleDeletePainting.bind(this), true);

        img.setAttribute('src', data.url);

        container.appendChild(img);
        container.appendChild(actions);

        wrap.appendChild(container);
        return wrap;
    },

    doImageSave : function (data) {
        var imageHTML = this.createImageHtml(data),
            doc = this.base.options.ownerDocument;

        this.base.restoreSelection();

        var selectionBaseNode = doc.getSelection().focusNode;
        this.pasteHTML(imageHTML.childNodes[0], selectionBaseNode);

        // Update toolbar -> hide this form
        this.base.checkSelection();
    },

    pasteHTML: function (newNode, node) {
        var parent = node.parentNode;
        var son = node;
        while(!this.hasClass(parent, 'interpret-content')){
            son = parent;
            parent = son.parentNode;
        }

        var sibling = son.nextSibling;
        if (sibling){
            parent.insertBefore(newNode, sibling);
        } else {
            parent.insertBefore(newNode, son);
        }
    },

    hasClass: function (element, cls) {
        return (' ' + element.className + ' ').indexOf(' ' + cls + ' ') > -1;
    }
}

ImageExtension = derives(MediumEditor.statics.AnchorExtension, ImageDerived);
