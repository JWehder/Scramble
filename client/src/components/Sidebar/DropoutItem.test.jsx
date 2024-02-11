import { render, screen } from '@testing-library/react';
import DropoutItem from './DropoutItem';

describe('DropoutItem Component', () => {
  it('renders the dropoutItem component', () => {
    // Mock userData for testing
    const userData =
    {
      "firstName": "Jane",
      "lastName": "Smith",
      "messages": [
        "Hey there!",
        "Hey there!",
        "Hey there!"
      ]
    };

    // Render the component with the mock userData
    const { container } = render(<DropoutItem type="Messages" userData={userData.messages} />);

    // container is defined
    expect(container).toBeDefined();
  });

  it('renders correct number of message components based on userData length', () => {

    // Mock userData for testing
    const userData =
    {
      "firstName": "Jane",
      "lastName": "Smith",
      "messages": [
        "Hey there!",
        "Hey there!",
        "Hey there!"
      ]
    };

    render(<DropoutItem type="Messages" userData={userData.messages} />);

    // Get all rendered Message components
    const renderedMessages = screen.getAllByText(/Hey there!/);

    // Check if the number of rendered components matches the length of userData (up to a maximum of 3)
    const expectedComponentCount = Math.min(userData.messages.length, 3);
    expect(renderedMessages.length).toBe(expectedComponentCount);
  }) 

  it('renders correct number of message components based on userData length', () => {

    // Mock userData for testing
    const userData =
    {
      "firstName": "Jane",
      "lastName": "Smith",
      "leagues": [
        {
        "name": "Jake's League",
        "team1Name": "Jake's team"
        },
        {
          "name": "Jake's League",
          "team1Name": "Jake's team"
        },
        {
          "name": "Jake's League",
          "team1Name": "Jake's team"
        }
      ]
    };

    render(<DropoutItem type="Teams & Leagues" data={userData.leagues} />);

    // Get all rendered Message components
    const renderedMessages = screen.getAllByText(/Jake's team/);

    // Check if the number of rendered components matches the length of userData (up to a maximum of 3)
    const expectedComponentCount = Math.min(userData.messages.length, 3);
    expect(renderedMessages.length).toBe(expectedComponentCount);
  }) 
});

