/*global FB*/
import fb_logo from '../../../../assets/Facebook_Logo_Primary.png';
import React, { Component } from 'react';
import axios from 'axios';

class FacebookLoginButton extends Component {
    async fetchFacebookAppId() {
        try {
          const response = await axios.get('/api/get_facebook_appId');
          // Access the data from the response
          const facebookAppId = response.data.facebook_app_id;
          return facebookAppId;
        } catch (error) {
          // Handle any errors
          console.error('Error fetching Facebook App ID:', error);
          throw error;
        }
    }

    async componentDidMount() {
        const appId = await this.fetchFacebookAppId();
        // Dynamically add Facebook SDK script
        const script = document.createElement('script');
        script.src = 'https://connect.facebook.net/en_US/sdk.js';
        script.async = true;
        script.onload = () => {
            // Initialize the Facebook SDK once the script is loaded
            window.fbAsyncInit = () => {
                FB.init({
                    appId: `${appId}`,
                    cookie: true,
                    xfbml: true,
                    version: 'v3.2',
                    _https: true
                });
            };
            // Log page view event
            FB.AppEvents.logPageView();
        };
        document.body.appendChild(script);
    }

    handleFacebookLogin = () => {
        // Perform Facebook login actions here
        FB.login(response => {
            // Handle login response
            if (response.authResponse) {
                console.log('User is logged in');
            } else {
                console.log('User cancelled login or did not fully authorize.');
            }
        }, { scope: 'email' }); // Specify the required permissions here
    };

    render() {
        return (
            <>
                <button
                className="flex justify-center items-center bg-light hover:brightness-110 border border-gray-300 text-gray-700 py-2 px-4 rounded-full focus:outline-none focus:shadow-outline"
                onClick={this.handleFacebookLogin}
                >
                    <img 
                    src={fb_logo} 
                    alt="facebook logo" 
                    className="w-9 h-9 mr-2"

                    />
                    <span>
                        {this.props.buttonText}
                    </span>
                </button>
            </>
        );
    }
}

export default FacebookLoginButton;
