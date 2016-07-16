    /**
     Copyright 2014-2015 Amazon.com, Inc. or its affiliates. All Rights Reserved.

     Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file except in compliance with the License. A copy of the License is located at

     http://aws.amazon.com/apache2.0/

     or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
     */

    /**
     * This sample shows how to create a simple Trivia skill with a multiple choice format. The skill
     * supports 1 player at a time, and does not support games across sessions.
     */

    'use strict';

    /**
     * When editing your questions pay attention to your punctuation. Make sure you use question marks or periods.
     * Make sure the first answer is the correct one. Set at least 4 answers, any extras will be shuffled in.
     */
    var productAttribs = {
        "samsung galaxy" : {
            "plans" : [
                "Verizon monthly twenty dollar, unlimited call, ten gb data",
                "AT&T month twenty five dollars, unlimited call, ten gb data"
            ],
            "best_plan" : 1
        },

        "iphone six" : {
            "plans" : [
                "Verizon monthly thirty dollar, unlimited call, ten gb data",
                "AT&T month twenty five dollars, unlimited call, ten gb data"
            ],
            "best_plan" : 2
        }
    };

    // Route the incoming request based on type (LaunchRequest, IntentRequest,
    // etc.) The JSON body of the request is provided in the event parameter.
    exports.handler = function (event, context) {
        try {
            console.log("event.session.application.applicationId=" + event.session.application.applicationId);

            /**
             * Uncomment this if statement and populate with your skill's application ID to
             * prevent someone else from configuring a skill that sends requests to this function.
             */

    //     if (event.session.application.applicationId !== "amzn1.echo-sdk-ams.app.05aecccb3-1461-48fb-a008-822ddrt6b516") {
    //         context.fail("Invalid Application ID");
    //      }

            if (event.session.new) {
                onSessionStarted({requestId: event.request.requestId}, event.session);
            }

            if (event.request.type === "LaunchRequest") {
                onLaunch(event.request,
                    event.session,
                    function callback(sessionAttributes, speechletResponse) {
                        context.succeed(buildResponse(sessionAttributes, speechletResponse));
                    });
            } else if (event.request.type === "IntentRequest") {
                onIntent(event.request,
                    event.session,
                    function callback(sessionAttributes, speechletResponse) {
                        context.succeed(buildResponse(sessionAttributes, speechletResponse));
                    });
            } else if (event.request.type === "SessionEndedRequest") {
                onSessionEnded(event.request, event.session);
                context.succeed();
            }
        } catch (e) {
            context.fail("Exception: " + e);
        }
    };

    /**
     * Called when the session starts.
     */
    function onSessionStarted(sessionStartedRequest, session) {
        console.log("onSessionStarted requestId=" + sessionStartedRequest.requestId
            + ", sessionId=" + session.sessionId);

        // add any session init logic here
    }

    /**
     * Called when the user invokes the skill without specifying what they want.
     */
    function onLaunch(launchRequest, session, callback) {
        console.log("onLaunch requestId=" + launchRequest.requestId
            + ", sessionId=" + session.sessionId);

        getWelcomeResponse(callback);
    }

    /**
     * Called when the user specifies an intent for this skill.
     */
    function onIntent(intentRequest, session, callback) {
        console.log("onIntent requestId=" + intentRequest.requestId
            + ", sessionId=" + session.sessionId);

        var intent = intentRequest.intent,
            intentName = intentRequest.intent.name;

        // handle yes/no intent after the user has been prompted
        if (session.attributes && session.attributes.userPromptedToContinue) {
            delete session.attributes.userPromptedToContinue;
            if ("AMAZON.NoIntent" === intentName) {
                handleFinishSessionRequest(intent, session, callback);
            } else if ("AMAZON.YesIntent" === intentName) {
                handleRepeatRequest(intent, session, callback);
            }
        }

        console.log("Inent name ", intentName);

        // dispatch custom intents to handlers here
        if ("ProductInfoIntent" === intentName) {
            handleProductRequest(intent, session, callback);
        } else if ("ProductOnlyIntent" === intentName) {
            handleProductRequest(intent, session, callback);
        } else if ("ProductAttribIntent" === intentName) {
            handleInfoRequest(intent, session, callback);
        } else if ("AMAZON.StartOverIntent" === intentName) {
            getWelcomeResponse(callback);
        } else if ("AMAZON.RepeatIntent" === intentName) {
            handleRepeatRequest(intent, session, callback);
        } else if ("AMAZON.HelpIntent" === intentName) {
            handleGetHelpRequest(intent, session, callback);
        } else if ("AMAZON.StopIntent" === intentName) {
            handleFinishSessionRequest(intent, session, callback);
        } else if ("AMAZON.CancelIntent" === intentName) {
            handleFinishSessionRequest(intent, session, callback);
        } else {
            throw "Invalid intent";
        }
    }

    /**
     * Called when the user ends the session.
     * Is not called when the skill returns shouldEndSession=true.
     */
    function onSessionEnded(sessionEndedRequest, session) {
        console.log("onSessionEnded requestId=" + sessionEndedRequest.requestId
            + ", sessionId=" + session.sessionId);

        // Add any cleanup logic here
    }

    // ------- Skill specific business logic -------
    var CARD_TITLE = "Store Assist"; // Be sure to change this for your skill.

    function getWelcomeResponse(callback) {
        var sessionAttributes = {},
            speechOutput = "Hello welcome to our store. How may I help you today? ",
            shouldEndSession = false,
            repromptText = "Hello, is there anything I can do for you today? ";

        sessionAttributes = {
            "speechOutput": repromptText,
            "repromptText": repromptText,
        };
        callback(sessionAttributes,
            buildSpeechletResponse(CARD_TITLE, speechOutput, repromptText, shouldEndSession));
    }

    function handleProductRequest(intent, session, callback) {
        var speechOutput = "";
        var sessionAttributes = {};
        var productName = getProductName(intent);

        if (!productName || !(productName in productAttribs)) {
            speechOutput = "Unfortunately, we don't have this item. Do you like to know about some other product";
        } else {
            sessionAttributes.productName = productName;
            speechOutput = "Certainly I can tell you more about " + productName + 
                " What you would like to know, the price or the available plans?";
        }
        callback(sessionAttributes,
            buildSpeechletResponse(CARD_TITLE, speechOutput, speechOutput, false));
    }

    function handleInfoRequest(intent, session, callback) {
        var attribName = "", speechOutput = "";
        var sessionAttributes = session.attributes;
        var productName = session.attributes && session.attributes.productName;

        if (!productName) {
            speechOutput = "I didn't get, which item you are looking for.";
        } else {
            speechOutput =  "I don't know about the product feature you would like to know. " +
                "Do you mind if I call a sales representative to help you";

            var attribSlotFilled = intent.slots && intent.slots.Attribute && intent.slots.Attribute.value;
            console.log("Intent name ", intent.name, "Intent slots ", intent.slots, attribSlotFilled);

            if (attribSlotFilled) {
                attribName = intent.slots.Attribute.value;
                var attribs = productAttribs[productName];
                console.log("Attribute Name ", attribName);

                var planKeys = ["plan", "plans", "price"];
                var bestPlanKeys = ["best plan", "best plans"];


                if (bestPlanKeys.indexOf(attribName) >=0 ) {
                    speechOutput = "Our best plan for " + productName + " is ";
                    speechOutput += attribs.plans[attribs.best_plan];
                }  else if (planKeys.indexOf(attribName) >=0 ) {
                    speechOutput == "Available plans for " + productName + " are ";
                    speechOutput = attribs["plans"].join(" ");
                }
            }
        }

        callback(sessionAttributes,
            buildSpeechletResponse(CARD_TITLE, speechOutput, speechOutput, false));

    }

    function handleRepeatRequest(intent, session, callback) {
        // Repeat the previous speechOutput and repromptText from the session attributes if available
        // else start a new game session
        if (!session.attributes || !session.attributes.speechOutput) {
            getWelcomeResponse(callback);
        } else {
            callback(session.attributes,
                buildSpeechletResponseWithoutCard(session.attributes.speechOutput, session.attributes.repromptText, false));
        }
    }

    function handleFinishSessionRequest(intent, session, callback) {
        // End the session with a "Good bye!" if the user wants to quit the game
        callback(session.attributes,
            buildSpeechletResponseWithoutCard("Good bye!", "", true));
    }

    function getProductName(intent) {
        var productName;
        var productSlotFilled = intent.slots && intent.slots.Product && intent.slots.Product.value;
        if (productSlotFilled) {
            productName = intent.slots.Product.value.toLowerCase();
        }
        console.log("Product Name ", productName);
        return productName;
    }
    // ------- Helper functions to build responses -------


    function buildSpeechletResponse(title, output, repromptText, shouldEndSession) {
        return {
            outputSpeech: {
                type: "PlainText",
                text: output
            },
            card: {
                type: "Simple",
                title: title,
                content: output
            },
            reprompt: {
                outputSpeech: {
                    type: "PlainText",
                    text: repromptText
                }
            },
            shouldEndSession: shouldEndSession
        };
    }

    function buildSpeechletResponseWithoutCard(output, repromptText, shouldEndSession) {
        return {
            outputSpeech: {
                type: "PlainText",
                text: output
            },
            reprompt: {
                outputSpeech: {
                    type: "PlainText",
                    text: repromptText
                }
            },
            shouldEndSession: shouldEndSession
        };
    }

    function buildResponse(sessionAttributes, speechletResponse) {
        return {
            version: "1.0",
            sessionAttributes: sessionAttributes,
            response: speechletResponse
        };
    }