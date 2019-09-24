'use strict';

const e = React.createElement;
const base_url = 'https://localhost:5000/diseases';

/*
class FlavorForm extends React.Component {
  constructor(props) {
    super(props);
    this.state = {value: 'coconut'};
    
    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleChange(event) {
    this.setState({value: event.target.value});
  }

  handleSubmit(event) {
    alert('Your favorite flavor is: ' + this.state.value);
    event.preventDefault();
  }

  render() {
    return (
      <form onSubmit={this.handleSubmit}>
        <label>
          Pick your favorite flavor:
          <select value={this.state.value} onChange={this.handleChange}>
            <option value="grapefruit">Grapefruit</option>
            <option value="lime">Lime</option>
            <option value="coconut">Coconut</option>
            <option value="mango">Mango</option>
          </select>
        </label>
        <input type="submit" value="Submit" />
      </form>
    );
  }
}
*/

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

const domContainer = document.querySelector('#like_button_container');

function DiseasesList(props) {
  const diseases = props.diseases;
  const listItems = diseases.map((disease) =>
    <li key={disease}>{disease}</li>
  );

  return (<ul>{listItems}</ul>);
}

fetch('/diseases')
  .then(response => {
    if (response.status != 200) {
      console.log("Server Error: " + response.text());
      return;
    }
    response.json()
      .then(data => {
        console.log('THERE');
        console.log(data['diseases']);
        ReactDOM.render(
          <DiseasesList diseases={data['diseases']}/>,
          domContainer
        );
      });
  })
  .catch(error => console.log('Fetch error: ' + error)
  );

// const domContainer = document.querySelector('#like_button_container');
// ReactDOM.render(e(LikeButton), domContainer);
