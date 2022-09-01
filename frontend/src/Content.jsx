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
    this.setState({isLoading: true})
    const randomDelay = Math.random() * 10000;
    setTimeout(() => {
      this.setState({
        isLoading: false,
        results: randomDelay
      })
    },
    randomDelay);
  }
  requestServer() {
    this.setState({isLoading: true})
    fetch('http://localhost:8000', {mode: 'cors'}).then(response => {
      this.setState({isLoading: false})
    })
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
        Request was delayed {this.state.results} ms
      </div>
    )
  }

  render() {
    return (
      <div>
        <h1>React Plugin Demo App</h1>
        <Button onClick={() => this.buttonHandler()} style={{marginBottom: '20px'}}>
          Run Timer
        </Button>
        <div id="results">
          {this.renderResults()}
        </div>
        <Button onClick={() => this.requestServer()} style={{marginBottom: '20px'}}>
          Make Request
        </Button>
      </div>
    )
  }
}

export default Content;
