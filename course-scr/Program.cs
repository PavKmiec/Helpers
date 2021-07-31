using System;
using System.Collections.Generic;
using Newtonsoft.Json;
using OpenQA.Selenium;
using OpenQA.Selenium.Chrome;
using System.Text.RegularExpressions;
using System.IO;

namespace scr
{
    // Install from nuget : selenuum web driver
    class Program
    {
        static void Main(string[] args)
        {
            // Chrome option instance
            var options = new ChromeOptions();
            // something I just had to do to fix error related to my own PC
            options.AddArguments("--disable-gpu");
            
            // new ChromeDriver that will allow to browse/navigate the web
            var driver = new ChromeDriver(options);
            // this url with filters outputs: Full-Time courses sorted A-Z
            var Url = "https://www.cityofglasgowcollege.ac.uk/course-search?sort_by=field_template_reference_field_qualification&sort_order=ASC&f%5B0%5D=field_template_reference%253Afield_mode_of_study%3A139&page=";
            // initial page number is 0 (for handling pagination)
            var pageNumber = 0;

            
            //create list to store course details
            List<Course> lstcourse = new List<Course>();

            // While loop to enable adding a page number for each iteration
            // therefore allowing us to navigate pagination
            do
            {
            //navigate to url
            driver.Navigate().GoToUrl(Url + pageNumber);

            //variable to keep course titles by HTML class name
            var courseNames = driver.FindElementsByClassName("panel-course-results__course-title");

            // for each element that it found write it's text value to a file and console
            foreach (var course in courseNames) 
            {
                try
                {
                    
                        //intialise variables
                        string titleWithLevel = "";
                        string title = "";
                        string level = "";
                        var listOfSkills = new List<string>();

                        //create string from found text
                        titleWithLevel = course.Text;

                        //check if level is HNC
                        if (titleWithLevel.Contains("HNC") == true) {
                            //split string into title and level
                            string[] split = Regex.Split(titleWithLevel, " HNC");
                            //set title and level to strings
                            title = split[0];
                            level = "HNC";
                        }
                        //check if level is HND
                        else if (titleWithLevel.Contains("HND") == true) {
                            //split string into title and level
                            string[] split = Regex.Split(titleWithLevel, " HND");
                            //set title and level to strings
                            title = split[0];
                            level = "HND";
                        }
                        //check if level is NC
                        else if (titleWithLevel.Contains("NC") == true) {
                            //split string into title and level
                            string[] split = Regex.Split(titleWithLevel, "NC");
                            //set title and level to strings
                            title = split[0];
                            level = "NC";
                        }
                        //check if level is NQ
                        else if (titleWithLevel.Contains("NQ") == true) {
                            //split string into title and level
                            string[] split = Regex.Split(titleWithLevel, "NQ");
                            //set title and level to strings
                            title = split[0];
                            level = "NQ";
                        }
                        //check if level is BA (Hons)
                        else if (titleWithLevel.Contains("BA (Hons)") == true) {
                            //split string into title and level
                            string[] split = Regex.Split(titleWithLevel, "BA (Hons)");
                            //set title and level to strings
                            title = split[0];
                            level = "BA (Hons)";
                        }
                        //BA
                        else if (titleWithLevel.Contains("BA") == true) {
                            //split string into title and level
                            string[] split = Regex.Split(titleWithLevel, "BA");
                            //set title and level to strings
                            title = split[0];
                            level = "BA";
                        }
                        //Access
                        else if (titleWithLevel.Contains("Access") == true) {
                            //split string into title and level
                            string[] split = Regex.Split(titleWithLevel, "Access");
                            //set title and level to strings
                            title = split[0];
                            level = "Access";
                        }
                        //Scottish Professional Diploma
                        else if (titleWithLevel.Contains("Scottish Professional Diploma") == true) {
                            //split string into title and level
                            string[] split = Regex.Split(titleWithLevel, "Scottish Professional Diploma");
                            //set title and level to strings
                            title = split[0];
                            level = "Scottish Professional Diploma";
                        }
                        //NPA
                        else if (titleWithLevel.Contains("NPA") == true) {
                            //split string into title and level
                            string[] split = Regex.Split(titleWithLevel, "NPA");
                            //set title and level to strings
                            title = split[0];
                            level = "NPA";
                        }
                        //otherwise set level to other (to be expanded)
                        else
                        {
                            title = titleWithLevel;
                            level = "Other";
                        }
                        //add course to list
                        lstcourse.Add(new Course() { Title = title, Level = level, Skill = listOfSkills.ToArray() });
                    
                }
                catch(Exception ex)
                {
                    throw new ApplicationException("Error: ", ex);
                }
            }
            pageNumber++;
            
        // do this until page number is 27 (the last result page at the time) 
        } while (pageNumber < 28);

        //convert list to json
        string output = JsonConvert.SerializeObject(lstcourse);


        //display json
        Console.WriteLine(output);

        

        using (System.IO.StreamWriter file = File.CreateText(@"curses.json"))
        {
          file.Write(output);
        }



        // TODO - remove the (SCQF level...) thing

        }
    }

    public class Course
    {
        public string Title { get; set; }
        public string Level { get; set; }

        public string[] Skill { get; set; }
    }
}
