#pragma once
#include "JuceHeader.h"
#include "PluginProcessor.h"




class OtherLookAndFeel : public juce::LookAndFeel_V4, public juce::Component
{

public:
	void drawRotarySlider(juce::Graphics& g, int x, int y, int width, int height, float sliderPos, float rotaryStartAngle,
		float rotaryEndAngle, juce::Slider& slider) override;

};


class CustomKnob : public juce::Component,
	public juce::Slider::Listener
{
public:
	CustomKnob(const juce::String& knobID, NeuralPluginAudioProcessor& p);
	void paint(juce::Graphics& g) override;
	void resized() override;
	void sliderValueChanged(juce::Slider* slider) override;

private:
	OtherLookAndFeel otherLookAndFeel;
	NeuralPluginAudioProcessor& audioProcessor;
    juce::Slider knob;
	juce::String knobComponentID;

	JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(CustomKnob)
};

