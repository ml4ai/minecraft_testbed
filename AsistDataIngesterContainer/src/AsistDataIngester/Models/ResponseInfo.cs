using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace AsistDataIngester.Models
{
    public class ResponseInfo
    {
        public DateTime StartDate { get; set; }
        public DateTime EndDate { get; set; }
        public int Status { get; set; }
        public int Progress { get; set; }
        public int Duration { get; set; }
        public int Finished { get; set; }
        public DateTime RecordedDate { get; set; }
    }
}
