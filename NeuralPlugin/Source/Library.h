#pragma once
#include "JuceHeader.h"
class Library : public juce::Component
{
public:
	Library();
	void paint(juce::Graphics& g) override;
	void resized() override;

private:
	juce::Label label;

	JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(Library)
};

