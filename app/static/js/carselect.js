var make_selector = '#make';
var municipeCssSelector = '#city';
var provinceDefaultText = 'Provincia';
var municipeDefaultText = 'Municipio';

var makes = [{
  name: '1',
  code: 1
}, {
  name: '2',
  code: 2
}, {
  name: '3',
  code: 3
}];


var municipes = [{
  name: '1-1',
  cod_prov: 1
}, {
  name: '1-2',
  cod_prov: 1
}, {
  name: '1-3',
  cod_prov: 1
}, {
  name: '2-1',
  cod_prov: 2
}, {
  name: '2-2',
  cod_prov: 2
}, {
  name: '2-3',
  cod_prov: 2
}, {
  name: '3-1',
  cod_prov: 3
}, {
  name: '3-2',
  cod_prov: 3
}, {
  name: '3-3',
  cod_prov: 3
}];

$(document).ready(function() {
  console.log("READY");
  // Set default text
  $(make_selector).append($('<option>').text(provinceDefaultText).attr('value', -1));
  $(municipeCssSelector).append($('<option>').text(municipeDefaultText).attr('value', -1));

  // Populate make select
  $.each(makes, function(number, province) {
    $(make_selector).append($('<option>').text(province.name).attr('value', province.code));
  });

  // When selected province changes, populate municipe select
  $(make_selector).change(function() {
    var selectedProvince = this.value;
    $(municipeCssSelector).empty();
    $(municipeCssSelector).append($('<option>').text(municipeDefaultText).attr('value', -1));
    $.each(municipes, function(number, municipe) {
      if (municipe.cod_prov == selectedProvince) {
        $(municipeCssSelector).append($('<option>').text(municipe.name).attr('value', number.toString()));
      }
    });
    $(municipeCssSelector).selectpicker('refresh');
    $(municipeCssSelector).selectpicker('render');
  });
});