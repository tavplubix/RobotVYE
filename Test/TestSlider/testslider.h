#ifndef TESTSLIDER_H
#define TESTSLIDER_H

#include <QtWidgets/QMainWindow>
#include <QTimer>
#include "ui_testslider.h"
#include "IntervalSlider.h"
#include "MyIntervalSlider.h"

class TestSlider : public QMainWindow
{
	Q_OBJECT

public:
	TestSlider(QWidget *parent = 0);
	~TestSlider();

private:
	QTimer timer;
	MyIntervalSlider *slider;
	Ui::TestSliderClass ui;
};

#endif // TESTSLIDER_H
