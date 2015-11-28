#include "testslider.h"
#include <QStyleFactory>

TestSlider::TestSlider(QWidget *parent)
	: QMainWindow(parent)
{
	ui.setupUi(this);
	slider = new MyIntervalSlider(this);
	ui.horizontalSlider->setStyle(QStyleFactory::create("Fusion"));
	ui.centralWidget->setLayout(ui.verticalLayout);
	slider->setMinimum(0);
	slider->setMaximum(255);
	ui.verticalLayout->addWidget(slider);
	slider->show();

	bool connected = connect(slider, &MyIntervalSlider::lowerValueChanged, this, [&](int val){
		//int v = slider->value();
		//int alt_v = slider->upperValue();
		QString s = "Lower: " + QString::number(val);
		ui.lowerLabel->setText(s);
	});

	connect(slider, &MyIntervalSlider::upperValueChanged, this, [&](){
		//int v = slider->value();
		//int alt_v = slider->upperValue();
		int val = slider->upperValue();
		QString s = "Upper: " + QString::number(val);
		ui.upperLabel->setText(s);
	});

	slider->setLowerValue(50);
	slider->setUpperValue(100);

	timer.setInterval(100);
	connect(&timer, &QTimer::timeout, this, [&](){
		QPoint cursorPos = mapFromGlobal(QCursor::pos());
		QString cs = "Cursor Position.x = " + QString::number(cursorPos.x());
		cs += " Cursor Position.y = " + QString::number(cursorPos.y());

		QString ss = "Lower = " + QString::number(slider->lowerValue()) + " Upper = " + QString::number(slider->upperValue());
		ui.posLabel->setText(ss);
		ui.NativePosLabel->setText(cs);

	});
	timer.start();
}

TestSlider::~TestSlider()
{

}
