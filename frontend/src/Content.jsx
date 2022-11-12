import React from 'react';
import { Button} from 'reactstrap';
import { BaseOpenTelemetryComponent } from '@opentelemetry/plugin-react-load'

class Content extends BaseOpenTelemetryComponent {
  constructor(props){
    super(props)
    this.state = {
      results: null,
      isLoading: false
    }
  }

  componentDidMount(){
    // Example, do something here
  }

  buttonHandler() {
    this.setState({isLoading: true, results: null})
    fetch('http://api.lvh.me/api/users', {mode: 'cors'})
      .then((response) => response.json())
      .then((data) => {
        this.setState({
          isLoading: false,
          results: data
        })
      })
  }

  userList(list) {
    const userList = list.map((user, index) => {
      return (
        <li key={user.id}>
          {user.username}: {user.email}
        </li>
      );
    });

    return <ul>{userList}</ul>;
  }

  renderResults(){
    if(this.state.isLoading){
      return <div> Loading results...</div>;
    }
    if (!this.state.results){
      return (
        <div>No Results</div>
      )
    }
    return (
      <div>
        response:
        {this.userList(this.state.results.users)}
      </div>
    )
  }

  render() {
    return (
      <div>
        <h1>React OpenTelemetry Demo App</h1>
        <Button onClick={() => this.buttonHandler()} style={{marginBottom: '20px'}}>
          Make Request
        </Button>
        <div id="results">
          {this.renderResults()}
        </div>
      </div>
    )
  }
}

export default Content;
