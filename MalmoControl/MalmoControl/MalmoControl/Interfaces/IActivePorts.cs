using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using MalmoControl.DTO;

namespace MalmoControl.Interfaces
{
    public interface IActivePorts
    {
        ListDTO Ports {get; set;}
        string malmoUp {get; set;}
    }
}
