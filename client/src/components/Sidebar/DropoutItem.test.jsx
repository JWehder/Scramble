import { render, screen } from '@testing-library/react';
import DropoutItem from './DropoutItem';

describe('DropoutItem Component', () => {
  it('renders the dropoutItem component', () => {
    // Render the component with the mock userData
    const { container } = render(<DropoutItem type="Messages" userData={userData} />);

    // container is defined
    expect(container).toBeDefined();
  });

  it('renders correct number of components based on userData length', () => {

    // Mock userData for testing
    const userData = [
      {
        "firstName": "Jane",
        "lastName": "Smith",
        "messages": [
          "Hey there!",
          "Hey there!",
          "Hey there!"
        ]
      },
    ]

    render(<DropoutItem type="Messages" userData={userData.messages} />);

    // Get all rendered Message components
    const renderedMessages = screen.getAllByText(/Hey there!/);

    // Check if the number of rendered components matches the length of userData (up to a maximum of 3)
    const expectedComponentCount = Math.min(userData.length, 3);
    expect(renderedMessages.length).toBe(expectedComponentCount);
  }) 
});

