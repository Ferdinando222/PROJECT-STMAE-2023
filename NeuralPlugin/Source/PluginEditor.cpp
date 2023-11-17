/*
  ==============================================================================

    This file contains the basic framework code for a JUCE plugin editor.

  ==============================================================================
*/

#include "PluginProcessor.h"
#include "PluginEditor.h"

//==============================================================================
NeuralPluginAudioProcessorEditor::NeuralPluginAudioProcessorEditor (NeuralPluginAudioProcessor& p)
    : AudioProcessorEditor (&p), audioProcessor (p)
{
    // Make sure that before the constructor has finished, you've set the
    // editor's size to whatever you need it to be.
    setSize(600, 500);
    setBackground(juce::Colours::darkgrey);
    //Create Library
    addAndMakeVisible(library);
    addAndMakeVisible(knob1);
    addAndMakeVisible(knob2);
    addAndMakeVisible(knob3);

    //Create and configure a "Save model" button
    addAndMakeVisible(save);
    save.addListener(this);
    save.setButtonText("Save Model");

    // Create and configure an "Open Model" button
    addAndMakeVisible(open);
    open.addListener(this);
    open.setButtonText("Open Model");
}

NeuralPluginAudioProcessorEditor::~NeuralPluginAudioProcessorEditor()
{
}

//==============================================================================
void NeuralPluginAudioProcessorEditor::paint (juce::Graphics& g)
{
    // (Our component is opaque, so we must completely fill the background with a solid colour)
    g.fillAll (backgroundColour);

    g.setColour (juce::Colours::white);
    g.setFont (15.0f);

    // Add labels to the main component
    addAndMakeVisible(knobLabel1);
    addAndMakeVisible(knobLabel2);
    addAndMakeVisible(knobLabel3);

    // Set label texts
    knobLabel1.setText("Volume", juce::NotificationType::dontSendNotification);
    knobLabel2.setText("Tone", juce::NotificationType::dontSendNotification);
    knobLabel3.setText("Saturation", juce::NotificationType::dontSendNotification);
  
    knobLabel1.attachToComponent(knob1, false);
    knobLabel2.attachToComponent(knob2, false);
    knobLabel3.attachToComponent(knob3, false);






}


void NeuralPluginAudioProcessorEditor::resized()
{
    juce::Rectangle<int> bounds = getLocalBounds();
    // This is generally where you'll want to lay out the positions of any
    // subcomponents in your editor..
    float rowHeight = getHeight() / 5;


    // Position the knobs horizontally at the top
    knob1->setBounds(0, getHeight() / 3, getWidth() / 4, rowHeight * 1.5);
    knob2->setBounds(getWidth() / 4, getHeight() / 3, getWidth() / 4, rowHeight * 1.5);
    knob3->setBounds(getWidth() / 2, getHeight() / 3, getWidth() / 4, rowHeight * 1.5);

    //Position of the buttons

    open.setBounds(getWidth() / 4, getHeight() - rowHeight * 1.5, getWidth() / 4, rowHeight * 1.5);

    save.setBounds(getWidth() / 2, getHeight() - rowHeight * 1.5, getWidth() / 4, rowHeight * 1.5);


    //Position of Library
    library.setBounds(getWidth()/1.3, 0, getWidth() / 4, getHeight());
}

void NeuralPluginAudioProcessorEditor::buttonClicked(juce::Button* button)
{
    if(button == &open)
    {
        juce::FileChooser fileChooser("Select a file to open...",
            juce::File::getSpecialLocation(juce::File::userHomeDirectory),
            "*.json*");

        if (fileChooser.browseForFileToOpen())
        {
            juce::File selectedFile = fileChooser.getResult();
            juce::AlertWindow::showMessageBoxAsync(juce::AlertWindow::InfoIcon,
                "File Selected",
                "You selected the file:\n" + selectedFile.getFullPathName());
            auto path = selectedFile.getFullPathName().toRawUTF8();
            audioProcessor.setFilePath(path);
        }
    }

    if (button == &save)
    {
        audioProcessor.saveModel();
    }

}

void NeuralPluginAudioProcessorEditor::setBackground(juce::Colour colour)
{
    backgroundColour = colour;
}


