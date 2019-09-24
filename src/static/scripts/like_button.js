'use strict';

// const e = React.createElement;
const base_url = 'https://localhost:5000/diseases';

/*
class LikeButton extends React.Component {
  constructor(props) {
    super(props);
    this.state = { liked: false };
  }

  render() {
    if (this.state.liked) {
      return 'You liked this.';
    }

    return e (
      'button',
      { onClick: () => this.setState({ liked: true }) },
      'Like'
    );
  }
}
*/


fetch('/diseases')
  .then(response => {
    if (response.status != 200) {
      console.log("Server Error: " + response.text());
      return;
    }
    console.log(response.json()['diseases'])
  })
  .catch(error => console.log('Fetch error: ' + error)
  );

// const domContainer = document.querySelector('#like_button_container');
// ReactDOM.render(e(LikeButton), domContainer);
