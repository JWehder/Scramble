import { render, screen } from '@testing-library/react';
import DropoutItem from './DropoutItem';


test('renders correct number of components based on userData length', () => {
    // Mock userData for testing
    const userData = [1, 2, 3, 4]; // For example, userData length is 4

    // Render the component with the mock userData
    render(<DropoutItem type="Messages" userData={userData} />);

    // Get all rendered components
    const renderedComponents = screen.getAllByTestId('rendered-component');

    // Check if the number of rendered components matches the length of userData (up to a maximum of 3)
    const expectedComponentCount = Math.min(userData.length, 3);
    expect(renderedComponents.length).toBe(expectedComponentCount);
});
