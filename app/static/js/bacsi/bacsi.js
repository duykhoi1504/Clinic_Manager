
                    function addMedicine() {
                        var name = document.getElementById("medicineName").value;

                         var quantity = document.getElementById("quantity").value;
                        if (name !== "" && quantity !== "") {
                            var medicineTable = document.getElementById("medicine_list_datas");
                            var rowCount = medicineTable.rows.length;

                            // Thêm dòng mới vào bảng
                            var newRow = medicineTable.insertRow(rowCount);
                            var cellCount = medicineTable.rows[0].cells.length;

                            // Thêm ô STT
                            var cell1 = newRow.insertCell(0);
                            cell1.innerHTML = rowCount;

                            // Thêm ô Tên thuốc
                            var cell2 = newRow.insertCell(1);
                            cell2.innerHTML = name;

                            // Thêm ô Đơn vị (tạm thời để làm ví dụ)
                            var cell3 = newRow.insertCell(2);
                            cell3.innerHTML = "Đơn vị";

                            // Thêm ô Số lượng (tạm thời để làm ví dụ)
                            var cell4 = newRow.insertCell(3);
                            cell4.innerHTML = quantity;

                            // Thêm ô Cách dùng (tạm thời để làm ví dụ)
                            var cell5 = newRow.insertCell(4);
                            cell5.innerHTML = "Cách dùng";

                             // Thêm ô Thao tác (nút Xóa)
                            var cell6 = newRow.insertCell(5);
                            cell6.innerHTML = "<button onclick=\"deleteRow(this)\">Xóa</button>";

                            document.getElementById("medicineName").value = "";
                            document.getElementById("quantity").value = "";

                        } else {
                            alert("Vui lòng nhập đầy đủ thông tin thuốc.");
                        }
                    }

                    function cancelMedicine() {
                        document.getElementById("medicineName").value = "";

                         document.getElementById("quantity").value = "";
                    }
                     function deleteRow(button) {
                        // Xóa dòng khi người dùng ấn nút Xóa
                        var row = button.parentNode.parentNode;
                        row.parentNode.removeChild(row);
    }
