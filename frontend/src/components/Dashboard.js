import React, { useState, useEffect, useRef } from 'react';
import { apisAPI } from '../utils/api';
import { toast } from 'react-toastify';
import { Plus, Edit2, Trash2, Eye, Calendar, Check, X } from 'lucide-react';
import APIModal from './APIModal';
import APIDetailsModal from './APIDetailsModal';

const Dashboard = () => {
    const [apis, setApis] = useState([]);
    const [loading, setLoading] = useState(true);
    const [showModal, setShowModal] = useState(false);
    const [showDetailsModal, setShowDetailsModal] = useState(false);
    const [selectedApi, setSelectedApi] = useState(null);
    const [page, setPage] = useState(1);
    const [totalPages, setTotalPages] = useState(1);

    const [filters, setFilters] = useState({
        search: "",
        method: "",
        status: "",
        dateFrom: "",
        dateTo: "",
        dateField: "created_at",
    });

    const [sort, setSort] = useState({
        by: "created_at",
        order: "desc",
    });

    const [searchHistory, setSearchHistory] = useState([]);
    const [isSearchFocused, setIsSearchFocused] = useState(false);
    const [showDatePicker, setShowDatePicker] = useState(false);
    const datePickerRef = useRef(null);
    const [selectedApis, setSelectedApis] = useState([]);

    // Handle clicking outside the date picker
    useEffect(() => {
        const handleClickOutside = (event) => {
            if (showDatePicker && datePickerRef.current && !datePickerRef.current.contains(event.target)) {
                setShowDatePicker(false);
            }
        };

        if (showDatePicker) {
            document.addEventListener('mousedown', handleClickOutside);
        }

        return () => {
            document.removeEventListener('mousedown', handleClickOutside);
        };
    }, [showDatePicker]);

    // Fetch APIs
    const fetchApis = async () => {
        setLoading(true);
        try {
            const response = await apisAPI.getAll({
                page,
                limit: 10,
                search: filters.search,
                method: filters.method,
                status: filters.status,
                dateFrom: filters.dateFrom,
                dateTo: filters.dateTo,
                dateField: filters.dateField,
                sortBy: sort.by,
                sortOrder: sort.order,
            });

            setApis(response.data.apis);
            setTotalPages(response.data.pages);
        } catch (error) {
            toast.error('Failed to fetch APIs');
            console.error('Fetch error:', error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchApis();
        setSelectedApis([]);
    }, [page, filters.method, filters.status, filters.dateFrom, filters.dateTo, filters.dateField, sort.by, sort.order]);

    useEffect(() => {
        const timer = setTimeout(() => {
            fetchApis();
        }, 300);

        return () => clearTimeout(timer);
    }, [filters.search]);

    useEffect(() => {
        if (!filters.search.trim() || filters.search.length < 3) return;

        const autoSaveTimer = setTimeout(() => {
            saveToSearchHistory(filters.search);
        }, 2000);

        return () => clearTimeout(autoSaveTimer);
    }, [filters.search]);

    const saveToSearchHistory = (term) => {
        if (term.trim() && term.length > 1) {
            setSearchHistory((prev) =>
                [term, ...prev.filter(s => s !== term)].slice(0, 5)
            );
        }
    };

    const handleSearchKeyPress = (e) => {
        if (e.key === 'Enter') {
            saveToSearchHistory(filters.search);
            setIsSearchFocused(false);
        }
    };

    const handleSearchBlur = () => {
        setTimeout(() => {
            setIsSearchFocused(false);
            if (filters.search.trim() && filters.search.length > 2) {
                saveToSearchHistory(filters.search);
            }
        }, 200);
    };

    //Get today's date in local timezone
    const getLocalDateString = (date) => {
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');
        return `${year}-${month}-${day}`;
    };

    //Date range preset options with correct local dates
    const applyDatePreset = (preset) => {
        const today = new Date();
        let dateFrom = '';
        let dateTo = getLocalDateString(today);

        switch (preset) {
            case 'today':
                dateFrom = dateTo;
                break;
            case 'yesterday':
                const yesterday = new Date(today);
                yesterday.setDate(yesterday.getDate() - 1);
                dateFrom = getLocalDateString(yesterday);
                dateTo = dateFrom;
                break;
            case 'last7days':
                const last7 = new Date(today);
                last7.setDate(last7.getDate() - 7);
                dateFrom = getLocalDateString(last7);
                break;
            case 'last30days':
                const last30 = new Date(today);
                last30.setDate(last30.getDate() - 30);
                dateFrom = getLocalDateString(last30);
                break;
            case 'thisMonth':
                const firstDay = new Date(today.getFullYear(), today.getMonth(), 1);
                dateFrom = getLocalDateString(firstDay);
                break;
            case 'lastMonth':
                const lastMonthFirst = new Date(today.getFullYear(), today.getMonth() - 1, 1);
                const lastMonthLast = new Date(today.getFullYear(), today.getMonth(), 0);
                dateFrom = getLocalDateString(lastMonthFirst);
                dateTo = getLocalDateString(lastMonthLast);
                break;
            default:
                break;
        }

        setFilters({ ...filters, dateFrom, dateTo });
    };

    const handleDateRangeApply = () => {
        if (filters.dateFrom && filters.dateTo) {
            const fromDate = new Date(filters.dateFrom);
            const toDate = new Date(filters.dateTo);

            if (fromDate > toDate) {
                toast.error('Start date cannot be after end date');
                return;
            }
        }

        setShowDatePicker(false);
        setPage(1);
    };

    const handleDateRangeClear = () => {
        setFilters({ ...filters, dateFrom: "", dateTo: "" });
        setShowDatePicker(false);
    };

    const handleCreate = () => {
        setSelectedApi(null);
        setShowModal(true);
    };

    const handleEdit = (api) => {
        if (filters.search.trim() && filters.search.length >= 3) {
            saveToSearchHistory(filters.search);
        }
        setSelectedApi(api);
        setShowModal(true);
    };

    const handleView = (api) => {
        if (filters.search.trim() && filters.search.length >= 3) {
            saveToSearchHistory(filters.search);
        }
        setSelectedApi(api);
        setShowDetailsModal(true);
    };

    const handleDelete = async (id) => {
        if (filters.search.trim() && filters.search.length >= 3) {
            saveToSearchHistory(filters.search);
        }
        if (window.confirm('Are you sure you want to delete this API?')) {
            try {
                await apisAPI.delete(id);
                toast.success('API deleted successfully');
                fetchApis();
            } catch (error) {
                toast.error('Failed to delete API');
            }
        }
    };

    const handleModalClose = (refresh) => {
        setShowModal(false);
        setSelectedApi(null);
        if (refresh) {
            fetchApis();
        }
    };

    const getDateRangeDisplay = () => {
        if (!filters.dateFrom && !filters.dateTo) return '';

        const formatDate = (dateStr) => {
            if (!dateStr) return '';
            try {
                const date = new Date(dateStr + 'T00:00:00');
                if (isNaN(date.getTime())) return dateStr;
                return date.toLocaleDateString('en-US', {
                    month: 'short',
                    day: 'numeric',
                    year: 'numeric'
                });
            } catch (e) {
                return dateStr;
            }
        };

        if (filters.dateFrom && filters.dateTo) {
            const from = new Date(filters.dateFrom);
            const to = new Date(filters.dateTo);
            if (from > to) {
                return '⚠️ Invalid';
            }
            return `${formatDate(filters.dateFrom)} - ${formatDate(filters.dateTo)}`;
        } else if (filters.dateFrom) {
            return `From ${formatDate(filters.dateFrom)}`;
        } else {
            return `Until ${formatDate(filters.dateTo)}`;
        }
    };

    const activeFiltersCount = [
        filters.method,
        filters.status,
        filters.dateFrom || filters.dateTo
    ].filter(Boolean).length;

    // Bulk Actions
    const handleSelectApi = (apiId) => {
        setSelectedApis(prev => {
            if (prev.includes(apiId)) {
                return prev.filter(id => id !== apiId);
            } else {
                return [...prev, apiId];
            }
        });
    };

    const handleSelectAll = () => {
        if (selectedApis.length === apis.length) {
            setSelectedApis([]);
        } else {
            setSelectedApis(apis.map(api => api._id));
        }
    };

    const isAllSelected = apis.length > 0 && selectedApis.length === apis.length;
    const isSomeSelected = selectedApis.length > 0 && selectedApis.length < apis.length;

    const handleBulkDelete = async () => {
        if (selectedApis.length === 0) {
            toast.warning('Please select APIs to delete');
            return;
        }

        if (!window.confirm(`Delete ${selectedApis.length} API(s)?`)) {
            return;
        }

        try {
            const deletePromises = selectedApis.map(id => apisAPI.delete(id));
            await Promise.all(deletePromises);

            toast.success(`Deleted ${selectedApis.length} API(s)`);
            setSelectedApis([]);
            fetchApis();
        } catch (error) {
            toast.error('Failed to delete some APIs');
            console.error('Bulk delete error:', error);
        }
    };

    const handleBulkStatusChange = async (newStatus) => {
        if (selectedApis.length === 0) {
            toast.warning('Please select APIs to update');
            return;
        }

        try {
            const updatePromises = selectedApis.map(id =>
                apisAPI.update(id, { status: newStatus })
            );
            await Promise.all(updatePromises);

            const statusText = newStatus === 'active' ? 'activated' : 'deactivated';
            toast.success(`${statusText.charAt(0).toUpperCase() + statusText.slice(1)} ${selectedApis.length} API(s)`);
            setSelectedApis([]);
            fetchApis();
        } catch (error) {
            toast.error('Failed to update some APIs');
            console.error('Bulk status change error:', error);
        }
    };

    const handleClearSelection = () => {
        setSelectedApis([]);
    };

    const handleSortChange = (field, newOrder) => {
        if (!newOrder) {
            if (sort.by === field) {
                setSort({ by: "created_at", order: "desc" });
            }
        } else {
            setSort({ by: field, order: newOrder });
        }
        setPage(1);
    };

    return (
        <div className="container">
            {/* Header */}
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
                <h1>My APIs</h1>
                <button className="btn btn-primary" onClick={handleCreate}>
                    <Plus size={18} style={{ marginRight: '5px' }} />
                    Create API
                </button>
            </div>

            {/* Bulk Actions Bar */}
            {selectedApis.length > 0 && (
                <div className="bulk-bar">
                    <div className="bulk-info">
                        <Check size={16} />
                        <span>{selectedApis.length} selected</span>
                    </div>
                    <div className="bulk-btns">
                        <button className="btn-xs btn-success" onClick={() => handleBulkStatusChange('active')}>
                            Activate
                        </button>
                        <button className="btn-xs btn-warning" onClick={() => handleBulkStatusChange('inactive')}>
                            Deactivate
                        </button>
                        <button className="btn-xs btn-danger" onClick={handleBulkDelete}>
                            <Trash2 size={14} /> Delete
                        </button>
                        <button className="btn-xs btn-secondary" onClick={handleClearSelection}>
                            <X size={14} /> Clear
                        </button>
                    </div>
                </div>
            )}

            {/* Compact Search + Filters */}
            <div className="card-compact">
                {/* Search */}
                <div style={{ position: 'relative', marginBottom: '10px' }}>
                    <input
                        type="text"
                        placeholder="🔍 Search APIs..."
                        value={filters.search}
                        onChange={(e) => {
                            const value = e.target.value;
                            setFilters({ ...filters, search: value });
                            if (value === '') {
                                e.target.blur();
                                setIsSearchFocused(false);
                            }
                        }}
                        onKeyPress={handleSearchKeyPress}
                        onFocus={() => setIsSearchFocused(true)}
                        onBlur={handleSearchBlur}
                        className="input-compact"
                    />

                    {isSearchFocused && searchHistory.length > 0 && !filters.search.trim() && (
                        <div className="search-history">
                            {searchHistory.map((term, index) => (
                                <div
                                    key={index}
                                    className="search-history-item"
                                    onMouseDown={(e) => {
                                        e.preventDefault();
                                        setFilters({ ...filters, search: term });
                                        setIsSearchFocused(false);
                                    }}
                                >
                                    🕒 {term}
                                </div>
                            ))}
                        </div>
                    )}
                </div>

                {/* Compact Filters Row */}
                <div className="filters-compact">
                    <div className="filters-left">
                        <span className="label-sm">Filters{activeFiltersCount > 0 && ` (${activeFiltersCount})`}:</span>

                        <select
                            value={filters.method}
                            onChange={(e) => setFilters({ ...filters, method: e.target.value })}
                            className="select-compact"
                        >
                            <option value="">Method</option>
                            <option>GET</option>
                            <option>POST</option>
                            <option>PUT</option>
                            <option>DELETE</option>
                            <option>PATCH</option>
                        </select>

                        <select
                            value={filters.status}
                            onChange={(e) => setFilters({ ...filters, status: e.target.value })}
                            className="select-compact"
                        >
                            <option value="">Status</option>
                            <option value="active">Active</option>
                            <option value="inactive">Inactive</option>
                        </select>

                        {/* Compact Date Picker */}
                        <div style={{ position: 'relative' }} ref={datePickerRef}>
                            <button
                                className={`btn-compact ${(filters.dateFrom || filters.dateTo) ? 'active' : ''}`}
                                onClick={() => setShowDatePicker(!showDatePicker)}
                            >
                                <Calendar size={14} />
                                <span>{(filters.dateFrom || filters.dateTo) ? getDateRangeDisplay() : 'Date'}</span>
                            </button>

                            {showDatePicker && (
                                <div className="date-dropdown">
                                    <div className="date-header">Filter by Date</div>

                                    {/* Date Type */}
                                    <div className="date-section">
                                        <label className="date-label">Date Type:</label>
                                        <div className="date-type-btns">
                                            <button
                                                className={`btn-date-type ${filters.dateField === 'created_at' ? 'active' : ''}`}
                                                onClick={() => setFilters({ ...filters, dateField: 'created_at' })}
                                            >
                                                Created
                                            </button>
                                            <button
                                                className={`btn-date-type ${filters.dateField === 'updated_at' ? 'active' : ''}`}
                                                onClick={() => setFilters({ ...filters, dateField: 'updated_at' })}
                                            >
                                                Updated
                                            </button>
                                        </div>
                                    </div>

                                    {/* Quick Presets */}
                                    <div className="date-section">
                                        <label className="date-label">Quick Select:</label>
                                        <div className="preset-grid">
                                            <button className="btn-preset" onClick={() => applyDatePreset('today')}>Today</button>
                                            <button className="btn-preset" onClick={() => applyDatePreset('yesterday')}>Yesterday</button>
                                            <button className="btn-preset" onClick={() => applyDatePreset('last7days')}>Last 7 Days</button>
                                            <button className="btn-preset" onClick={() => applyDatePreset('last30days')}>Last 30 Days</button>
                                            <button className="btn-preset" onClick={() => applyDatePreset('thisMonth')}>This Month</button>
                                            <button className="btn-preset" onClick={() => applyDatePreset('lastMonth')}>Last Month</button>
                                        </div>
                                    </div>

                                    {/* Custom Range */}
                                    <div className="date-section">
                                        <label className="date-label">From:</label>
                                        <input
                                            type="date"
                                            value={filters.dateFrom}
                                            onChange={(e) => setFilters({ ...filters, dateFrom: e.target.value })}
                                            max={filters.dateTo || undefined}
                                            className="date-input"
                                        />
                                    </div>

                                    <div className="date-section">
                                        <label className="date-label">To:</label>
                                        <input
                                            type="date"
                                            value={filters.dateTo}
                                            onChange={(e) => setFilters({ ...filters, dateTo: e.target.value })}
                                            min={filters.dateFrom || undefined}
                                            className="date-input"
                                        />
                                    </div>

                                    {/* Actions */}
                                    <div className="date-actions">
                                        <button className="btn-date-action secondary" onClick={handleDateRangeClear}>
                                            Clear
                                        </button>
                                        <button className="btn-date-action primary" onClick={handleDateRangeApply}>
                                            Apply
                                        </button>
                                    </div>
                                </div>
                            )}
                        </div>
                    </div>

                    {/* Compact Sort */}
                    <div className="sort-compact">
                        <span className="label-sm">Sort:</span>

                        <select
                            value={sort.by === "name" ? sort.order : ""}
                            onChange={(e) => handleSortChange("name", e.target.value)}
                            className="select-compact"
                        >
                            <option value="">Name</option>
                            <option value="asc">A → Z</option>
                            <option value="desc">Z → A</option>
                        </select>

                        <select
                            value={sort.by === "created_at" ? sort.order : ""}
                            onChange={(e) => handleSortChange("created_at", e.target.value)}
                            className="select-compact"
                        >
                            <option value="">Created</option>
                            <option value="desc">Newest</option>
                            <option value="asc">Oldest</option>
                        </select>

                        <select
                            value={sort.by === "updated_at" ? sort.order : ""}
                            onChange={(e) => handleSortChange("updated_at", e.target.value)}
                            className="select-compact"
                        >
                            <option value="">Updated</option>
                            <option value="desc">Recent</option>
                            <option value="asc">Oldest</option>
                        </select>

                        <select
                            value={sort.by === "usage_count" ? sort.order : ""}
                            onChange={(e) => handleSortChange("usage_count", e.target.value)}
                            className="select-compact"
                        >
                            <option value="">Usage</option>
                            <option value="desc">Most</option>
                            <option value="asc">Least</option>
                        </select>

                        <button
                            className="btn-reset"
                            title="Reset All"
                            onClick={() => {
                                setFilters({
                                    search: "",
                                    method: "",
                                    status: "",
                                    dateFrom: "",
                                    dateTo: "",
                                    dateField: "created_at"
                                });
                                setSort({ by: "created_at", order: "desc" });
                                setPage(1);
                            }}
                        >
                            ↺
                        </button>
                    </div>
                </div>
            </div>

            {loading ? (
                <div className="card" style={{ padding: "30px", textAlign: "center" }}>
                    Loading APIs…
                </div>
            ) : apis.length === 0 ? (
                <div className="card" style={{ textAlign: 'center', padding: '30px' }}>
                    <p>
                        No APIs found.
                        {activeFiltersCount > 0 ? ' Try adjusting your filters.' : ' Create your first API!'}
                    </p>
                </div>
            ) : (
                <>
                    <div className="card">
                        <table className="table">
                            <thead>
                                <tr>
                                    <th style={{ width: '40px' }}>
                                        <input
                                            type="checkbox"
                                            checked={isAllSelected}
                                            ref={input => {
                                                if (input) {
                                                    input.indeterminate = isSomeSelected;
                                                }
                                            }}
                                            onChange={handleSelectAll}
                                            style={{ cursor: 'pointer' }}
                                        />
                                    </th>
                                    <th>Name</th>
                                    <th>Method</th>
                                    <th>Endpoint</th>
                                    <th>Status</th>
                                    <th>Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                {apis.map((api) => (
                                    <tr
                                        key={api._id}
                                        className={selectedApis.includes(api._id) ? 'selected-row' : ''}
                                    >
                                        <td>
                                            <input
                                                type="checkbox"
                                                checked={selectedApis.includes(api._id)}
                                                onChange={() => handleSelectApi(api._id)}
                                                style={{ cursor: 'pointer' }}
                                            />
                                        </td>
                                        <td>{api.name}</td>
                                        <td>
                                            <span className={`badge badge-${api.method === 'GET' ? 'info' : api.method === 'POST' ? 'success' : 'warning'}`}>
                                                {api.method}
                                            </span>
                                        </td>
                                        <td style={{ maxWidth: '300px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                                            {api.endpoint}
                                        </td>
                                        <td>
                                            <span className={`badge badge-${api.status === 'active' ? 'success' : 'danger'}`}>
                                                {api.status}
                                            </span>
                                        </td>
                                        <td>
                                            <div style={{ display: 'flex', gap: '8px' }}>
                                                <button className="btn btn-secondary" style={{ padding: '4px 8px' }} onClick={() => handleView(api)}>
                                                    <Eye size={16} />
                                                </button>
                                                <button className="btn btn-primary" style={{ padding: '4px 8px' }} onClick={() => handleEdit(api)}>
                                                    <Edit2 size={16} />
                                                </button>
                                                <button className="btn btn-danger" style={{ padding: '4px 8px' }} onClick={() => handleDelete(api._id)}>
                                                    <Trash2 size={16} />
                                                </button>
                                            </div>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>

                    {totalPages > 1 && (
                        <div style={{ display: 'flex', justifyContent: 'center', gap: '10px', marginTop: '16px' }}>
                            <button
                                className="btn btn-secondary"
                                onClick={() => setPage(page - 1)}
                                disabled={page === 1}
                            >
                                Previous
                            </button>
                            <span style={{ padding: '8px 0', fontSize: '14px' }}>Page {page} of {totalPages}</span>
                            <button
                                className="btn btn-secondary"
                                onClick={() => setPage(page + 1)}
                                disabled={page === totalPages}
                            >
                                Next
                            </button>
                        </div>
                    )}
                </>
            )}

            {showModal && <APIModal api={selectedApi} onClose={handleModalClose} />}
            {showDetailsModal && <APIDetailsModal api={selectedApi} onClose={() => setShowDetailsModal(false)} />}

            <style>
                {`
/* Compact Card */
.card-compact {
  background: white;
  border-radius: 8px;
  padding: 12px;
  margin-bottom: 16px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

/* Compact Input */
.input-compact {
  width: 100%;
  padding: 8px 10px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
}

.input-compact:focus {
  outline: none;
  border-color: #3b82f6;
}

/* Compact Filters Row */
.filters-compact {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.filters-left,
.sort-compact {
  display: flex;
  align-items: center;
  gap: 6px;
  flex-wrap: wrap;
}

.label-sm {
  font-size: 13px;
  font-weight: 600;
  color: #555;
}

/* Compact Select */
.select-compact {
  padding: 5px 8px;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 13px;
  background: white;
  cursor: pointer;
}

.select-compact:focus {
  outline: none;
  border-color: #3b82f6;
}

/* Compact Button */
.btn-compact {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 5px 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
  background: white;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-compact:hover {
  background: #f9fafb;
}

.btn-compact.active {
  background: #3b82f6;
  color: white;
  border-color: #3b82f6;
}

.btn-reset {
  padding: 5px 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
  background: white;
  cursor: pointer;
  font-size: 14px;
}

.btn-reset:hover {
  background: #f3f4f6;
}

/* Date Dropdown - More Compact */
.date-dropdown {
  position: absolute;
  top: calc(100% + 6px);
  right: 0;
  background: white;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 12px;
  min-width: 280px;
  z-index: 1000;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

.date-header {
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 10px;
  color: #333;
}

.date-section {
  margin-bottom: 10px;
}

.date-label {
  display: block;
  font-size: 12px;
  font-weight: 600;
  color: #555;
  margin-bottom: 5px;
}

.date-type-btns {
  display: flex;
  gap: 6px;
}

.btn-date-type {
  flex: 1;
  padding: 5px 10px;
  border: 1px solid #ddd;
  background: white;
  border-radius: 5px;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-date-type:hover {
  background: #f3f4f6;
}

.btn-date-type.active {
  background: #3b82f6;
  color: white;
  border-color: #3b82f6;
}

.preset-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 5px;
}

.btn-preset {
  padding: 5px 10px;
  border: 1px solid #ddd;
  background: white;
  border-radius: 5px;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-preset:hover {
  background: #f3f4f6;
}

.date-input {
  width: 100%;
  padding: 5px 8px;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 12px;
}

.date-actions {
  display: flex;
  gap: 6px;
  margin-top: 10px;
  padding-top: 10px;
  border-top: 1px solid #eee;
}

.btn-date-action {
  flex: 1;
  padding: 6px 12px;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-date-action.secondary {
  background: white;
  color: #555;
}

.btn-date-action.primary {
  background: #3b82f6;
  color: white;
  border-color: #3b82f6;
}

.btn-date-action:hover {
  opacity: 0.9;
}

/* Search History */
.search-history {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: white;
  border: 1px solid #ddd;
  border-radius: 6px;
  margin-top: 2px;
  z-index: 1000;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  max-height: 180px;
  overflow-y: auto;
}

.search-history-item {
  padding: 8px 12px;
  cursor: pointer;
  font-size: 13px;
  color: #333;
  border-bottom: 1px solid #f0f0f0;
  transition: background 0.2s;
}

.search-history-item:last-child {
  border-bottom: none;
}

.search-history-item:hover {
  background: #f3f4f6;
}

/* Bulk Actions - More Compact */
.bulk-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #eff6ff;
  border: 1px solid #3b82f6;
  border-radius: 6px;
  padding: 8px 12px;
  margin-bottom: 12px;
  animation: slideDown 0.3s ease;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-8px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.bulk-info {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  font-weight: 600;
  color: #1e40af;
}

.bulk-btns {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}

.btn-xs {
  padding: 4px 8px;
  font-size: 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 3px;
  transition: all 0.2s;
}

.btn-xs.btn-success {
  background: #10b981;
  color: white;
}

.btn-xs.btn-warning {
  background: #f59e0b;
  color: white;
}

.btn-xs.btn-danger {
  background: #ef4444;
  color: white;
}

.btn-xs.btn-secondary {
  background: #6b7280;
  color: white;
}

.btn-xs:hover {
  opacity: 0.9;
}

/* Selected Row */
.selected-row {
  background-color: #eff6ff !important;
}

.table tbody tr.selected-row:hover {
  background-color: #dbeafe !important;
}

/* Checkbox */
input[type="checkbox"] {
  width: 16px;
  height: 16px;
  cursor: pointer;
}

/* Responsive */
@media (max-width: 768px) {
  .filters-compact {
    flex-direction: column;
    align-items: stretch;
  }
  
  .filters-left,
  .sort-compact {
    width: 100%;
    justify-content: flex-start;
  }
  
  .date-dropdown {
    left: 0;
    right: 0;
    min-width: auto;
  }

  .bulk-bar {
    flex-direction: column;
    gap: 8px;
  }

  .bulk-btns {
    width: 100%;
    justify-content: stretch;
  }

  .btn-xs {
    flex: 1;
  }
}
`}
            </style>
        </div>
    );
};

export default Dashboard;