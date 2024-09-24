using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace AsistDataIngester.Models
{
    public class SurveyInfo
    {
        public string Id { get; set; }
        public string Name { get; set; }
        public string OwnerId { get; set; }
        public DateTime LastModified { get; set; }
        public DateTime CreationDate { get; set; }
        public string IsActive { get; set; }
    }
}
