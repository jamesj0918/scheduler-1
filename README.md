# Scheduler
A lecture scheduler for university students. Built with Django 2.1.

## Features
* Provides a list of possible scenarios of lectures.
* Ability to create a break time in schedules.
* REST API support for various platforms.
* Categorizing lectures by searching lecture titles from [NAVER Book](https://book.naver.com/).

## API Endpoints
### Get a list of lectures
`GET /api/lectures/search/`

|Name|Type|Description|
|---|---|---|
|`search`|`string`|Parameter for search against: `title`, `department`, `professor`.|
|`page`|`int`|Page of the lecture list. Single page contains 100 lectures by default.|
|`id`|`int`|Unique identifier of the lecture. Not to be confused with `code`.|
|`code`|`string`|Integer-labeled code of the lecture. Multiple lectures can have a same `code`.|
|`title`|`string`|Title of the lecture. Note that this field is not for exact matching.|
|`point`|`float`|Point of the lecture. Starting from `0.5`.|
|`category`|`string`|Category of the lecture. See `categories` for more informations.|
|`subcategory`|`string`|Sub-category of the lecture. See `sub-categories` for more informations.|
|`classroom`|`string`|Classroom of the lecture.|
|`professor`|`string`|Professor of the lecture.|
|`lecture`|`list`|List of `id` of lectures. Result lectures will be filtered with the `timetable` from these lectures.|
|`timetable`|`list`|List of timetables. Format of `timetable` is `day:start:end`. (For example, Monday, Starts at 13:00, Ends at 15:00 would be `mon:1300:1500`)

### Get a list of possible lectures
`GET /api/lectures/query/`

|Name|Type|Description|
|---|---|---|
|`timetable`|`string`|Timetable to filter. Use the same format as above (`day:start:end`), but use comma for more than one filters. (`day:start:end, day:start:end, ...`)|
|`fixed`|`string`|Fixed lecture to filter. Use the `id`, and comma for more than one filters. Results will be contain these fixed lectures.|
|`selected`|`string`|Desired lecture that used for generating combination. Use the `code`, and comma for more than one filters. Note that more than 3 selected lectures would results huge performance decrease for now, due to slow server speed.|

### Get a list of unique lectures
`GET /api/lectures/unique/`
> NOTE: You can use same parameters from `/api/lectures/search/` here.

### Get a list of categories
`GET /api/category/`

### Get a list of sub-categories
`GET /api/subcategory/`

### Get a list of departments
`GET /api/department/`

## License
Licensed under the [MIT License](https://github.com/pellstrike/scheduler/blob/master/LICENSE.md).
