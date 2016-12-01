# pefinder Docker

This is a Docker image that will run PE-Finder to produce output for some input data file. 

Packages that need to be installed (e.g. seaborn and radnlp) have versions specified in case a future change breaks this code, you can see this in the top section of the [Dockerfile](Dockerfile).


## Getting Started
You should first [install Docker](https://docs.docker.com/engine/installation/) and then build the container:

    docker build -t vanessa/pefinder .


## Analyzing Reports
The function of the container is to take reports and produce a `.tsv` file with PEFinder classifications. Let's first run the container with the `--help` argument to see what arguments are needed:


	docker run vanessa/pefinder --help
	INFO:pefinder:radnlp version 0.2.0.8
	usage: cli.py [-h] --reports REPORTS [--report_field REPORT_FIELD]
		      [--id_field ID_FIELD] [--result_field RESULT_FIELD] --output
		      OUTPUT [--no-remap] [--run {mark,classify,analyze}]

	generate predictions for PE for a set of reports (impressions)

	optional arguments:
	  -h, --help            show this help message and exit
	  --reports REPORTS     Path to folder of reports, or tab separated text file
	  --report_field REPORT_FIELD
		                the header column that contains the text of interest
		                (default is report_text)
	  --id_field ID_FIELD   the header column that contains the id of the report
		                (default is report_id)
	  --result_field RESULT_FIELD
		                the field to save pefinder (chapman) result to, not
		                saved unless --no-remap is specified.
	  --output OUTPUT       Desired output file (.tsv)
	  --no-remap            don't remap multilabel PEFinder result to Stanford
		                labels
	  --run {mark,classify,analyze}
		                mark (mark), classify (classify) or mark and classify
		                (analyze) reports.


You are minimally going to need to provide `--reports`, and `--output`, which assumes that the report text is in a column called `report_text`, the report id is in a column called `report_id`, and you want to perform all actions (mark and classify) as the default for the `--run` command. The most basic running command we will use looks like this:


      docker run -v $PWD:/data vanessa/pefinder --reports /data/pefinder/data/stanford_data.csv --delim , --output /data/stanford_result.tsv


The `-v` argument means "volume" and it says that we want to map the present working directory (`$PWD`) to the folder in the container called `/data`. We do this so that we can read and write to `/data` in the container, and the result will appear in our present working directory. Otherwise, the result would remain in the container and we wouldn't have easy access to it. Note that the `--reports` input is also relative to `/data`, meaning that the input is located at `$PWD/pefinder/data/stanford_reports.csv`. The `--output` variable, then, is relative to inside of the container. By writing to `/data/stanford_result.tsv` we are going to see the file `stanford_data.tsv` appear in our `$PWD` because of the volume. Now, let's talk about what your options are for your reports input data.


### Reports
For your input data, you have two options:

1. *Folder*: a folder of raw text files, with each text file name assumed to be the report id, and the entire content the impression part of the report to analyze.
2. *File*: a single tab separated (`.tsv`) file with some field for the report text (default is assumed to be `report_text`) and report id (default is `report_id`).


### What if I want to change defaults?

- If you need to change the delimiter, specify it with the argument `--delim`
- If you need to change the default report text column name, specify it with the argument `--report_field`
- If you need to change the default report id column name, specify it with the argument `--report_id`


## Examples

### Analyzing Reports
Analyzing reports means marking and classification.

	docker run -v $PWD:/data vanessa/pefinder --reports /data/pefinder/data/stanford_data.csv --delim , --output /data/stanford_result.tsv
	INFO:pefinder:radnlp version 0.2.0.8
	INFO:pefinder:
	***STARTING PE-FINDER DOCKER****
	INFO:pefinder:Will use column report_text as report text.
	INFO:pefinder:Will use column report_id as report id.
	INFO:pefinder:reports path provided is /data/pefinder/data/stanford_data.csv
	INFO:pefinder:Analyzing 117816 reports, please wait...


### Marking Reports
This is an intermediate step that won't give you classification labels. You might do this to look at the data. The markup is output in the field `markup` of the results file.

	docker run -v $PWD:/data vanessa/pefinder --run mark --reports /data/pefinder/data/stanford_data.csv --delim , --output /data/stanford_result.tsv


### Classifying Reports
This is the final step to classify the markup (the `markup` column of your input data) and produce the classification. If you just want this classification, you should run the first example, Analyzing Reports.


	docker run -v $PWD:/data vanessa/pefinder --run classify --reports /data/pefinder/data/stanford_data.csv --delim , --output /data/stanford_result.tsv


## How do I shell into the container?
By default, running the container uses the `ENTRYPOINT`, meaning it is used as an executable and you do not enter the container. In the case that you want a container-based environment that is installed with the dependencies of PEFinder, or if you want to interactively work with the code, you may want to shell into the container. To do this, you can run the following:

      docker run vanessa/pefinder --entrypoint /bin/sh

If there is a running container (eg an analysis) and you want to open up another terminal on your local machine to look inside (while it's running!) you can do that too:

      docker exec -it vanessa/pefinder bash

This says we want to execute (exec) and (interactive)(terminal) for container with id (af21bf1d48a6) and run the command (bash)


## Why?
By "shipping" analyses in packages, meaning having a specification of all dependencies (python modules, data, etc.) we can be assured that the next person that runs our analysis will not run into system-specific differences. They won't have to install python or anaconda to run our notebook, and get a weird message about having the wrong kernel. They just need Docker, and then to run the image, and that's it. This is an important feature of reproducible workflows and analyses, and every piece of code that you work on (and tend to share) should have features like this.
