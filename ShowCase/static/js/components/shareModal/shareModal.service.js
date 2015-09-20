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

    function shareFacebook () {
        _updateHref('https://www.facebook.com/sharer/sharer.php', {
          u: window.location.href
        });
    };

    function shareTwitter (description) {
        return function () {
            _updateHref('https://twitter.com/intent/tweet', {
                text: description,
                url: window.location.href
            });
        }
    };

    function shareGoogle () {
        _updateHref('https://plus.google.com/share', {
            url: window.location.href
        });
    };

    function sharePinterest (description, image) {
        return function () {
            _updateHref('https://www.pinterest.com/pin/create/button', {
                url: window.location.href,
                media: image,
                description: description
            });
        }
    };

    function shareTumblr (description, image) {
        return function () {
            _updateHref('http://www.tumblr.com/share/photo', {
                clickthru: window.location.href,
                source: image,
                description: description
            });
        }
    };

    function shareViaEmail (subject, description) {
        return function () {
            _updateHref('mailto:', {
                subject: this.config.networks.email.title,
                body: this.config.networks.email.description
            });
        }
    };

    function shareReddit (title) {
        return function () {
            _updateHref('http://www.reddit.com/submit', {
                url: window.location.href,
                title: title
            });
        }
    };

    function shareWhatsapp (description) {
        return function () {
            _updateHref('whatsapp://send', {
                text: description + ' ' + window.location.href
            });
        }
    };

    var service = {};

    var pageActions = function (title, image) {
        return {
            'shareFacebook': shareFacebook,
            'shareTwitter': shareTwitter(title),
            'shareGoogle': shareGoogle,
            'shareWhatsapp': shareWhatsapp(title),
            'shareReddit': shareReddit(title),
            'sharePinterest': sharePinterest(title, image),
            'shareTumblr': shareTumblr(title, image)
        }
    };

    service.shareThisPage = function (title, image) {
        modalService.showModal({
            'templateUrl': '/static/js/components/shareModal/shareModal.tpl.html',
            'controller': 'shareModalController',
            'inputs' : {'actions': pageActions(title, image)}
        });
    };

    return service;
}]);