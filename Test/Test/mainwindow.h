#ifndef MAINWINDOW_H
#define MAINWINDOW_H

//Qt includes
#include <QFileDialog>
#include <QColorDialog>
#include <QMainWindow>
#include <QImage>
#include <QPixmap>
#include <QDebug>
#include <QPalette>
#include <QTimer>

//#include <QxtSpanSlider>
#include "IntervalSlider.h"

//OpenCV includes
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>

namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = 0);
    ~MainWindow();

private:
    Ui::MainWindow *ui;
    QColor qlower, qupper;
    QPixmap before, mask, after;
    QTimer timer;
    cv::VideoCapture capture;
    IntervalSlider *slider;

    void processImage(cv::Mat cvimage/*const QString &filename*/);
    QPixmap cvMatToQImage(const cv::Mat& cvm);


};

#endif // MAINWINDOW_H
