getTestCssFile = """h3.testName
{ text-align: center; }
#failed
{ color: red;}
#passed
{ color: green;}
#skipped
{ color: grey;}
div.invisible
{ display: none;}
table.testResults
{
    width: 100%;
    border-top-width: 2px;
    border-color: black;
    border-top-style: solid;
    border collapse: collapse;
}
div.testTdException
{ color: red; }
pre
{
    line-height: 13px;
    margin: 0;
    padding: 0;
}
"""

getClassCssFile = """#failed
{ color: red;}
#passed
{ color: green;}
#skipped
{ color: grey;}
div.className
{ text-align: left; }
table.clear
{
    width: 100%;
    border-bottom-width: 2px;
    border-bottom-style: solid;
    border-top-width: 2px;
    border-top-style: solid;
    border-color: black;
}
th
{
    text-align: center;
    background-color: #B0C4DE;
}
td.topLine
{
    border-top-width: 1px;
    border-top-style: solid;
}
td.topBottomLines
{
    border-bottom-width: 1px;
    border-bottom-style: solid;
    border-top-width: 1px;
    border-top-style: solid;
}
td.testName
{
    width: 90%;
    text-align: left;
}
td.configOrTest
{
    width: 1%;
    white-space: nowrap;
    text-align: left;
}
"""

getMainCssFile = """#failed
{ color: red;}
#passed
{ color: green;}
#skipped
{ color: grey;}
table.clear
{
    width: 100%;
    border-bottom-width: 2px;
    border-bottom-style: solid;
    border-top-width: 2px;
    border-top-style: solid;
    border-color: black;
}
th
{
    text-align: center;
    background-color: #B0C4DE;
}
td.suiteName
{
    text-align: left;
    width: 1%;
    white-space: nowrap;
    border-bottom-width: 1px;
    border-bottom-style: dotted;
}
td.pkgName
{
    text-align: left;
    width: 1%;
    white-space: nowrap;
    border-bottom-width: 1px;
    border-bottom-style: dotted;
}
td.className
{
    text-align: left;
    border-bottom-width: 1px;
    border-bottom-style: dotted;
}
td.subTests
{
    width: 10%;
    text-align: left;
}
td.duration
{
    width: 15%;
    text-align: left;
}
td.result
{
    width: 5%;
    text-align: left;
}
"""
