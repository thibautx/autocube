var React = require('react'),
    ReactDOM = requre('react-dom');

var button = React.DOM.button({
  className: "btn btn-lg btn-success",
  children: "Register"
});

ReactDOM.render(button, document.getElementById('content'));