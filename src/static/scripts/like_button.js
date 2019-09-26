'use strict';

const domContainer = document.querySelector('#engine');

class DoctorLimitSelection extends React.Component {
  constructor(props) {
    super(props);
    this.state = {top: 1, bottom: 0, error: 200, error_message: ''}
    this.maxDoctors = props.doctors;
    this.setTopLimit = this.setTopLimit.bind(this)
    this.setLowerLimit = this.setLowerLimit.bind(this)
    this.next = this.next.bind(this)
    this.back = this.back.bind(this)
  }

  back(event) {
    alert('This will take you directly back to disease selection.');
    fetchDiseases(200, '');
  }

  next(event) {
    console.log('Top: ' + this.state.top + ' Bottom: ' + this.state.bottom);
    let error_message = ''
    try {
      if (this.state.top > this.maxDoctors || this.state.top < 1) {
        error_message = 'Top must be between 1 and ' + this.maxDoctors;
        if (this.state.bottom < 0 || this.state.bottom > this.maxDoctors) {
          error_message += ', and bottom must be between 0 and ' + this.maxDoctors;
        }
      } else if (this.state.bottom < 0 || this.state.bottom > this.maxDoctors) {
        error_message = 'Bottom must be between 0 and ' + this.maxDoctors;
      }
    } catch {
      error_message += 'Both limits must be numbers'
    }

    if (error_message != '') {
      console.log(error_message);
      this.setState({error: 200, error_message: error_message});
      return;
    }
    console.log('Submit');
  }

  setTopLimit(event) {
    this.setState({top: event.target.value});
  }

  setLowerLimit(event) {
    this.setState({bottom: event.target.value});
  }

  render() {
    return (
      <div className="container">
        <h1 className="mt-5">Select Doctors</h1>
        <p className="lead">Select which doctors to target for your marketing scheme. You can pick from the top ranked doctors or bottom ranked for the specified disease, i.e. Top 5 and Bottom 3, means you will be able to see the top 5 ranked and bottom 3 ranked doctors. <b>The limit is {this.maxDoctors}</b>.</p>
        <div className="row m-3">
	  <div className="col-sm-6 mt-2 mb-3">
            <div className="form-group row">
	      <label htmlFor="top_limit" className="col-sm-4 col-form-label">From top:</label>
	      <div className="col-sm-8">
	        <input onChange={this.setTopLimit} id="top_limit" className="form-control" type="number" defaultValue="1" min="1" max="{this.maxDoctors}"/>
              </div>
            </div>
          </div>
	  <div className="col-sm-6 mt-2 mb-3">
	    <div className="row form-group">
	      <label htmlFor="bottom_limit" className="col-sm-4 col-form-label">From bottom:</label>
	      <div className="col-sm-8">
	        <input onChange={this.setLowerLimit} type="number" className="form-control" id="bottom_limit" defaultValue="0" min="1" max="{this.maxDoctors}"/>
              </div>
            </div>
          </div>
        </div>
        <div className="row m-2 mt-3">
          <div className="col-2">
            <span className="float-left">
              <button className="btn btn-outline-secondary" onClick={this.back}>Back</button>
	    </span>
          </div>
          <div className="col-8 text-center">
          </div>
          <div className="col-2">
            <span className="float-right">
              <button className="btn btn-outline-secondary" onClick={this.next}>Next</button>
            </span>
          </div>
        </div>
	<ErrorBar error={this.state.error} error_message={this.state.error_message}/>
      </div>
    );
  }
}

class ParameterSelectionForm extends React.Component {
  constructor(props) {
    super(props);
    this.params = props.params;
  }

  back(event) {
    fetchDiseases(200, '');
  }

  render() {
    const diseaseListItems = this.params.map((pair, index) =>
      <li key={index} className="list-group-item d-flex justify-content-between align-items-center">
        {pair.parameter}
        <span className="badge badge-primary badge-pill">
          {pair.importance}
        </span>
      </li>
    );
    return (
      <div className="container">
        <h1 className="mt-5">Select Parameters</h1>
        <p className="lead">These are all the parameters present in our database. Parameters which have already been selected for a disease have already been ticked and assigned an importance value when they were input. You can remove parameters by setting their importances to 0. All selected parameters are indicated by them having a value. Any change made below, will be updated in the database and set as the default parameter-importance values for this disease when you click <span className="bold font-italic">Next</span>. To add more parameters for a disease, click on the <span className="font-italic">Add/Update Diseases Info</span> tab.</p>
	<ul className="list-group list-group-flush m-3">
          {diseaseListItems}
	</ul>
        <div className="row m-2 mt-4">
          <div className="col-2">
            <span className="float-left">
              <button className="btn btn-outline-secondary" onClick={this.back}>Back</button>
	    </span>
          </div>
          <div className="col-8 text-center">
          </div>
          <div className="col-2">
            <span className="float-right">
              <button className="btn btn-outline-secondary">Next</button>
            </span>
          </div>
        </div>
	<ErrorBar error={200} error_message={""}/>
      </div>
    );
  }
}

class DiseaseSelectionForm extends React.Component {
  constructor(props) {
    super(props);
    this.state = {value: '',
	          error: props.error,
	          error_message: props.error_message};
    this.diseases = props.diseases;
    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleOptionSelection = this.handleOptionSelection.bind(this);
  }

  handleOptionSelection(event) {
    console.log(event.target.value);
    this.setState({value: event.target.value});
  }

  handleSubmit() {
    if (this.state.value == '' && this.state.error != 200) {
      this.setState({error_message: 'Error, contact admin to check the server'});
      return;
    }
    if (this.state.value == '' && this.state.error == 200) {
      console.log('Nothing is selected');
      this.setState({error: 200,
                     error_message: 'Input Error, nothing has been selected'});
      return;
    }
    console.log('The selected diseases is: ' + this.state.value);
    fetchParameters(this.state.value);
  }

  render() {
    let diseaseListItems;
    try {
      if (this.diseases) {
        console.log('NOT NULL');
        diseaseListItems = this.diseases.map((disease, index) =>
          <option key={index} value={disease}>{disease}</option>
        );
      } else {
        console.log('NULL');
        diseaseListItems = null;  //(<div></div>);
        console.log('HERE 2');
      }
    }
    catch {
      console.log('UNDEFINED');
      diseaseListItems = null;  // (<div></div>);
    }
    console.log(diseaseListItems);
    return (
      <div>
        <h1 className="mt-5">Select Disease</h1>
        <p className="lead">These are all the diseases present in the database. To add more, click on the <span className="font-italic">Add/Update Diseases Info</span> tab.</p>
	<div className="input-group">
          <select className="custom-select" onChange={this.handleOptionSelection}>
            <option value="">Choose...</option>
            {diseaseListItems}
          </select>
          <div className="input-group-append">
            <button className="btn btn-outline-secondary" onClick={this.handleSubmit}>Next</button>
          </div>
	</div>
	<ErrorBar error={this.state.error} error_message={this.state.error_message}/>
      </div>
    );
  }
}

function ErrorBar(props) {
  console.log(props.error + ' ' + props.error_message);
  if (props.error != 200) {
    return (
      <div className="mt-4 alert alert-danger">
        <strong>{props.error}</strong>: {props.error_message}
      </div>
    );
  }
  if (props.error_message != "OK" && props.error_message != "") {
    return (
      <div className="mt-2 alert alert-warning">
        {props.error_message}
      </div>
    );
  }
  return (<div/>);
}

function Loader(props) {
  return (
    <div className="d-flex justify-content-center mt-5">
      <div className="spinner-border spinner-border-lg" style={{width: '5rem', height: '5rem'}} role="status">
        <span className="sr-only">Loading...</span>
      </div>
    </div>
  );
}

function fetchDiseases(error, error_message) {
  ReactDOM.render(
    <Loader/>,
    domContainer
  );
  fetch('/diseases')
    .then(response => {
      const response_status = response.status;
      const response_statusText = response.statusText;
      if (response_status != 200) {
        const error_message = response_status + ' ' + response_statusText;
        ReactDOM.render(
          <DiseaseSelectionForm error={response_status}
            error_message={response_statusText}/>,
          domContainer
        );
        return;
      }
      if (error != 200) {
        response.json()
          .then(data => {
            console.log(data['diseases']);
            ReactDOM.render(
              <DiseaseSelectionForm diseases={data['diseases']} error={error}
                error_message={error_message}/>,
              domContainer
            );
          });
      } else {
        response.json()
          .then(data => {
            console.log(data['diseases']);
            ReactDOM.render(
              <DiseaseSelectionForm diseases={data['diseases']} error={response_status}
                error_message={response_statusText}/>,
              domContainer
            );
          });
      }
    })
    .catch(error => {
      const error_message = 'user end fetch error, could not get diseases';
      console.log('Fetch error: ' + error + ', could not get diseases')
      ReactDOM.render(
        <DiseaseSelectionForm error={0} error_message={error_message}/>,
        domContainer
      );
    });
}

function fetchParameters(disease) {
  console.log('fetching parameters for disease...');
  ReactDOM.render(
    <Loader/>,
    domContainer
  );
  fetch('/diseases/' + disease, {
    headers: {"Content-Type": "application/json; charset=utf-8"},
    method: 'POST'})
    .then(response => {
      if (response.status != 200) {
        const error_message = response.statusText;
        const error_code = response.status;
        console.log('Server Error' + error_code + ': ' + error_message);
        fetchDiseases('Server error', error_code + ' ' + error_message);
        return;
      }
      response.json()
        .then(data => {
          console.log(data);
          let sortedData = data.sort((a, b) => parseInt(b.importance) - parseInt(a.importance));
          ReactDOM.render(
            <ParameterSelectionForm params={sortedData}/>,
            domContainer
          );
	})
    })
    .catch(error => {
      console.log('Caught error: ' + error)
      fetchDiseases('Fetch error', 'cannot get disease parameters');
    });
}

function fetchDoctorLimitCriteria() {
  console.log('fetching max number of doctors to select from...');
  ReactDOM.render(
    <Loader/>,
    domContainer
  );
  fetch('/doctors/count')
    .then(response => { 
      if (response.status != 200) {
        const error_message = response.statusText;
        const error_code = response.status;
        console.log('Server Error' + error_code + ': ' + error_message);
        fetchParameters('Server error', error_code + ' ' + error_message);
        return;
      }
      response.json()
        .then(data =>
          ReactDOM.render(
            <DoctorLimitSelection doctors={data['count']}/>,
            domContainer
          )
	)
    })
}

$(document).ready(function() {
  console.log('Loaded page');
  // fetchDiseases(200, '');
  // fetchParameters('test disease 1');
  fetchDoctorLimitCriteria();
});
