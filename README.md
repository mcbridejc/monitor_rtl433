# monitor_rtl433

A wrapper to collect data from 433MHz wireless sensors using the rtl_433 command line utility, and make it available as metrics in [prometheus format](https://github.com/prometheus/docs/blob/master/content/docs/instrumenting/exposition_formats.md). 

## Requirements

This uses the [rtl_433](https://github.com/merbanan/rtl_433) project, which can support a variety of software defined radios, including the [RTL-SDR](https://www.rtl-sdr.com/), which is what I have used. 

## Setup

The `rtl_433` command line utility will listen for broadcasts at 434MHz using OOK modulation -- which is used by a variety of wireless environmental sensors, such as the [AcuRite 06002M Wireless Temperature and Humidity Sensor](https://www.amazon.com/gp/product/B00T0K8NXC) -- and spit them out stdout in a variety of convenient formats. This program is just a simple python wrapper that forks an rtl_433 process and collects its output, while running a webserver to serve out the collected data.

After installing the package, you can run it simply with `python -m monitor_rtl433`, and then visit `localhost:5000`.
Out-of-the box, the `/sensors` route will show raw data from any detected sensors, but the `/metrics` route will be blank. 

Setting up the `/metrics` routes requires a little more work to define which sensors you want to generate metrics from, and how they should be defined. See [examples/main.py](examples/main.py) for an example of how to create `MetricDescription` and `MetricFilter` objects and provide these to `montor_rtl433.run()`.

![Sensors Table](/images/example_sensors_table.png?raw=true "Sensors Table")