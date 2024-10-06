$(document).ready(function () {
    let applicantsAscending = true;
    let timePostedAscending = true;
    $("#collectDataButton").click(function () {
      const checkedLinks = [];
      $(".job-checkbox:checked").each(function () {
        const jobLink = $(this).closest("tr").find("a").attr("href");
        checkedLinks.push(jobLink);
      });

      let csvContent = "data:text/csv;charset=utf-8,Link\n";
      checkedLinks.forEach(function (link) {
        csvContent += link + "\r\n";
      });
      if (checkedLinks.length === 0) {
        alert("No links selected");
        return;
      }

      const encodedUri = encodeURI(csvContent);
      const linkElement = document.createElement("a");
      linkElement.setAttribute("href", encodedUri);
      linkElement.setAttribute("download", "job_links.csv");
      document.body.appendChild(linkElement);
      linkElement.click();
      document.body.removeChild(linkElement);
    });
    $("#sortApplicants").click(function () {
      sortTable(4, applicantsAscending);
      applicantsAscending = !applicantsAscending;
    });

    $("#sortTimePosted").click(function () {
      sortTable(5, timePostedAscending);
      timePostedAscending = !timePostedAscending;
    });

    $("#openPopupButton").click(function () {
      $("#popup").fadeIn();
    });

    $(".close").click(function () {
      $("#popup").fadeOut();
    });

    $("#applyFiltersButton").click(function () {
      applyFilters();
    });

    $("#applyPopupFiltersButton").click(function () {
      applyFilters();
    });

    $("#resetfilter").click(function () {
      $("#searchBar").val("");
      $("#minApplicants").val("");
      $("#maxApplicants").val("");
      $("#timePosted").val("");
      $("#city").val("");
      filterJobs("", 0, Infinity, "", "");
    });

    $("#allJobs").click(function () {
      $.ajax({
        url: "/jobs",
        method: "GET",
        success: function (data) {
          // Zakładam, że data zawiera HTML do wstawienia do tabeli
          $("#jobTableBody").html(data);
        },
        error: function (xhr, status, error) {
          console.error("Error fetching all jobs:", status, error);
        }
      });
    });

    function applyFilters() {
      const searchTerm = $("#searchBar").val().toLowerCase();
      const minApplicants = parseInt($("#minApplicants").val()) || 0;
      const maxApplicants = parseInt($("#maxApplicants").val()) || Infinity;
      const timePosted = $("#timePosted").val().toLowerCase();
      const city = $("#city").val().toLowerCase();

      filterJobs(
        searchTerm,
        minApplicants,
        maxApplicants,
        timePosted,
        city
      );
    }

    function filterJobs(
      searchTerm,
      minApplicants,
      maxApplicants,
      timePosted,
      city
    ) {
      const jobTable = document.getElementById("jobTable");
      const rows = jobTable.getElementsByTagName("tr");
      for (let i = 0; i < rows.length; i++) {
        const cells = rows[i].getElementsByTagName("td");
        let match = true;
        for (let j = 0; j < cells.length; j++) {
          if (cells[j]) {
            const cellText = cells[j].textContent || cells[j].innerText;
            if (
              j == 2 &&
              cellText.toLowerCase().indexOf(searchTerm) === -1
            ) {
              // Zmiana na kolumnę "Job Title"
              match = false;
            }
            if (j == 4) {
              const applicants = parseInt(cellText);
              if (
                (minApplicants && applicants < minApplicants) ||
                (maxApplicants && applicants > maxApplicants)
              ) {
                match = false;
              }
            }
            if (
              j == 5 &&
              cellText.toLowerCase().indexOf(timePosted) === -1
            ) {
              match = false;
            }
            if (j == 3 && cellText.toLowerCase().indexOf(city) === -1) {
              match = false;
            }
          }
        }
        rows[i].style.display = match ? "" : "none";
      }
    }
  });

  function parseTimePosted(text) {
    if (!text || text.toLowerCase() === "none") {
      return null;
    }

    const now = new Date();
    const [value, unit, ago] = text.split(" ");

    const number = parseInt(value);
    if (isNaN(number)) {
      return now;
    }

    switch (unit) {
      case "day":
      case "days":
        return new Date(now.setDate(now.getDate() - number));
      case "week":
      case "weeks":
        return new Date(now.setDate(now.getDate() - number * 7));
      case "month":
      case "months":
        return new Date(now.setMonth(now.getMonth() - number));
      case "year":
      case "years":
        return new Date(now.setFullYear(now.getFullYear() - number));
      default:
        return now;
    }
  }

  function sortTable(columnIndex, ascending) {
    const jobTable = document.getElementById("jobTable");
    const rows = Array.from(jobTable.getElementsByTagName("tr")).slice(1); // Pomijamy pierwszy wiersz nagłówka

    const sortedRows = rows.sort((a, b) => {
      const aText =
        a.getElementsByTagName("td")[columnIndex]?.innerText.trim() || "";
      const bText =
        b.getElementsByTagName("td")[columnIndex]?.innerText.trim() || "";

      if (columnIndex === 4) {
        // Applicants column
        const aApplicants = parseInt(aText) || 0;
        const bApplicants = parseInt(bText) || 0;
        return ascending
          ? aApplicants - bApplicants
          : bApplicants - aApplicants;
      } else if (columnIndex === 5) {
        // Time Posted column
        const aTimePosted = parseTimePosted(aText);
        const bTimePosted = parseTimePosted(bText);

        if (aTimePosted === null) return ascending ? 1 : -1;
        if (bTimePosted === null) return ascending ? -1 : 1;

        return ascending
          ? aTimePosted - bTimePosted
          : bTimePosted - aTimePosted;
      } else {
        return ascending
          ? aText.localeCompare(bText)
          : bText.localeCompare(aText);
      }
    });
    // Usuń istniejące wiersze
    while (jobTable.rows.length > 1) {
      jobTable.deleteRow(1);
    }

    // Dodaj posortowane wiersze
    sortedRows.forEach((row) => jobTable.appendChild(row));
  }