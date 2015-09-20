angular.module('module.shareModal')
.factory('shareModalService', ['$q', 'modalService', 'auth', function ($q, modalService, auth) {

    String.prototype.toRFC3986 = function () {
      var tmp = encodeURIComponent(this);
      tmp.replace(/[!'()*]/g, function (c) {
        return "%" + c.charCodeAt(0).toString(16);
      });
    };

    function _encode(str) {
      if (typeof str === "undefined" || str === null || _isEncoded(str)) return encodeURIComponent(str);else return str.toRFC3986();
    }

    function _isEncoded(str) {
      str = str.toRFC3986();
      return decodeURIComponent(str) !== str;
    }

    function _getUrl(url) {
      var _this = this;

      var encode = arguments.length <= 1 || arguments[1] === undefined ? false : arguments[1];
      var params = arguments.length <= 2 || arguments[2] === undefined ? {} : arguments[2];

      var qs = (function () {
        var results = [];
        var _iteratorNormalCompletion = true;
        var _didIteratorError = false;
        var _iteratorError = undefined;

        try {
          for (var _iterator = Object.keys(params)[Symbol.iterator](), _step; !(_iteratorNormalCompletion = (_step = _iterator.next()).done); _iteratorNormalCompletion = true) {
            var k = _step.value;

            var v = params[k];
            results.push(k + "=" + _encode(v));
          }
        } catch (err) {
          _didIteratorError = true;
          _iteratorError = err;
        } finally {
          try {
            if (!_iteratorNormalCompletion && _iterator["return"]) {
              _iterator["return"]();
            }
          } finally {
            if (_didIteratorError) {
              throw _iteratorError;
            }
          }
        }

        return results.join("&");
      })();

      if (qs) qs = "?" + qs;

      return url + qs;
    }

    function _updateHref(url, params) {
        var encode = url.indexOf("mailto:") >= 0;
        var url = _getUrl(url, !encode, params);
        var popup = {
            width: 500,
            height: 350
        };

        popup.top = screen.height / 2 - popup.height / 2;
        popup.left = screen.width / 2 - popup.width / 2;

        window.open(url, "targetWindow", "\n          toolbar=no,\n          location=no,\n          status=no,\n          menubar=no,\n          scrollbars=yes,\n          resizable=yes,\n          left=" + popup.left + ",\n          top=" + popup.top + ",\n          width=" + popup.width + ",\n          height=" + popup.height + "\n        ");
    }

    function shareFacebook (url) {
        return function () {
            _updateHref('https://www.facebook.com/sharer/sharer.php', {
              u: url
            });
        }
    };

    function shareTwitter (url, description) {
        return function () {
            _updateHref('https://twitter.com/intent/tweet', {
                text: description,
                url: url
            });
        }
    };

    function shareGoogle (url) {
        return function () {
            _updateHref('https://plus.google.com/share', {
                url: url
            });
        }
    };

    function sharePinterest (url, description, image) {
        return function () {
            _updateHref('https://www.pinterest.com/pin/create/button', {
                url: url,
                media: image,
                description: description
            });
        }
    };

    function shareTumblr (url, description, image) {
        return function () {
            _updateHref('http://www.tumblr.com/share/photo', {
                clickthru: url,
                source: image,
                description: description
            });
        }
    };

    function shareViaEmail (subject, description) {
        return function () {
            _updateHref('mailto:', {
                subject: subject,
                body: description
            });
        }
    };

    function shareReddit (url, title) {
        return function () {
            _updateHref('http://www.reddit.com/submit', {
                url: url,
                title: title
            });
        }
    };

    function shareWhatsapp (url, description) {
        return function () {
            _updateHref('whatsapp://send', {
                text: description + ' ' + url
            });
        }
    };

    var service = {};

    var shareActions = function (url, title, description, image) {
        return {
            'shareFacebook': shareFacebook(url),
            'shareTwitter': shareTwitter(url, title),
            'shareGoogle': shareGoogle(url),
            'shareWhatsapp': shareWhatsapp(url, title),
            'shareReddit': shareReddit(url, title),
            'sharePinterest': sharePinterest(url, title, image),
            'shareTumblr': shareTumblr(url, title, image),
            'shareViaEmail': shareViaEmail(title, description)
        }
    };

    service.shareThisPage = function (url, title, description, image) {
        modalService.showModal({
            'templateUrl': '/static/js/components/shareModal/shareModal.tpl.html',
            'controller': 'shareModalController',
            'inputs' : {'actions': shareActions(url, title, description, image)}
        });
    };

    return service;
}]);