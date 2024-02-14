import { render as rtlRender, screen } from '@testing-library/react';
import DropoutItem from './DropoutItem';
import { Provider } from 'react-redux';
import store from '../../../store';

const { leagues, messages, articles, games } = store.getState().users;

const render = component => rtlRender(
  <Provider store={store}>
    {component}
  </Provider>
);

describe('DropoutItem Component', () => {
  it('renders the dropoutItem component', () => {

    // Render the component with the mock userData
    const { container } = render(<DropoutItem type="Messages" />);

    // container is defined
    expect(container).toBeDefined();
  });

  it('renders correct number of messages components based on redux testing data length', () => {

    render(<DropoutItem type="Messages" />);

    // Get all rendered Message components
    const renderedMessages = screen.getAllByText(/Hey there!/);

    // Check if the number of rendered components matches the length of userData (up to a maximum of 3)
    const expectedComponentCount = Math.min(messages.length, 3);
    expect(renderedMessages.length).toBe(expectedComponentCount);
  }) 

  it('renders correct number of league components based on redux data length', () => {

    render(<DropoutItem type="Teams & Leagues" />);

    // Get all rendered Message components
    const renderedMessages = screen.getAllByText(/Jake's team/);

    // Check if the number of rendered components matches the length of userData (up to a maximum of 3)
    const expectedComponentCount = Math.min(leagues.length, 3);
    expect(renderedMessages.length).toBe(expectedComponentCount);
  }) 

  it('renders correct number of game components based on redux data length', () => {

    render(<DropoutItem type="Play" />);

    // loop through games and determine if they are on the screen
    const gameNames = games.map((gameName) => {
      if (screen.getAllByText(new RegExp(gameName))) {
        return gameName;
      }
    });

    // Check if the number of rendered components matches the length of userData (up to a maximum of 3)
    const expectedComponentCount = Math.min(gameNames.length, 3);
    expect(gameNames.length).toBe(expectedComponentCount);
  });
  
  it('renders correct number of article components based on redux data length', () => {

    render(<DropoutItem type="Articles" />);

    // loop through articles and determine if they are on the screen
    const articleNames = articles.map((article) => {
      if (screen.getAllByText(new RegExp(article.name))) {
        return article.name;
      }
    });

    // Check if the number of rendered components matches the length of redux data (up to a maximum of 3)
    const expectedComponentCount = Math.min(articleNames.length, 3);
    expect(articleNames.length).toBe(expectedComponentCount);
  });
});

